# -*- coding: utf-8 -*-
import datetime
import json
import requests

from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

from . import exceptions
from .compliance import fitbit_compliance_fix
from .utils import curry


class FitbitOauth2Client(object):
    API_ENDPOINT = "https://api.fitbit.com"
    AUTHORIZE_ENDPOINT = "https://www.fitbit.com"
    API_VERSION = 1

    request_token_url = "%s/oauth2/token" % API_ENDPOINT
    authorization_url = "%s/oauth2/authorize" % AUTHORIZE_ENDPOINT
    access_token_url = request_token_url
    refresh_token_url = request_token_url

    def __init__(self,
                 client_id,
                 client_secret,
                 access_token=None,
                 refresh_token=None,
                 expires_at=None,
                 refresh_cb=None,
                 redirect_uri=None,
                 *args,
                 **kwargs):

        self.client_id, self.client_secret = client_id, client_secret
        token = {}
        if access_token and refresh_token:
            token.update({
                'access_token': access_token,
                'refresh_token': refresh_token
            })
        if expires_at:
            token['expires_at'] = expires_at
        self.session = fitbit_compliance_fix(
            OAuth2Session(
                client_id,
                auto_refresh_url=self.refresh_token_url,
                token_updater=refresh_cb,
                token=token,
                redirect_uri=redirect_uri,
            ))
        self.timeout = kwargs.get("timeout", None)

    def _request(self, method, url, **kwargs):
        if self.timeout is not None and 'timeout' not in kwargs:
            kwargs['timeout'] = self.timeout

        try:
            response = self.session.request(method, url, **kwargs)

            if response.status_code == 401:
                d = json.loads(response.content.decode('utf8'))
                if d['errors'][0]['errorType'] == 'expired_token':
                    self.refresh_token()
                    response = self.session.request(method, url, **kwargs)

            return response
        except requests.Timeout as e:
            raise exceptions.Timeout(*e.args)

    def make_request(self, url, data=None, method=None, **kwargs):
        data = data or {}
        method = method or ('POST' if data else 'GET')
        response = self._request(method,
                                 url,
                                 data=data,
                                 client_id=self.client_id,
                                 client_secret=self.client_secret,
                                 **kwargs)

        exceptions.detect_and_raise_error(response)

        return response

    def authorize_token_url(self, scope=None, redirect_uri=None, **kwargs):
        self.session.scope = scope or [
            "activity",
            "nutrition",
            "heartrate",
            "location",
            "nutrition",
            "profile",
            "settings",
            "sleep",
            "social",
            "weight",
        ]

        if redirect_uri:
            self.session.redirect_uri = redirect_uri

        return self.session.authorization_url(self.authorization_url, **kwargs)

    def fetch_access_token(self, code, redirect_uri=None):
        if redirect_uri:
            self.session.redirect_uri = redirect_uri
        return self.session.fetch_token(self.access_token_url,
                                        username=self.client_id,
                                        password=self.client_secret,
                                        client_secret=self.client_secret,
                                        code=code)

    def refresh_token(self):
        token = {}
        if self.session.token_updater:
            token = self.session.refresh_token(self.refresh_token_url,
                                               auth=HTTPBasicAuth(
                                                   self.client_id,
                                                   self.client_secret))
            self.session.token_updater(token)

        return token


class Fitbit(object):
    JP = 'ja_JP'

    API_ENDPOINT = "https://api.fitbit.com"
    API_VERSION = 1
    WEEK_DAYS = [
        'SUNDAY', 'MONDAY', 'TUESDAY', 'WEDNESDAY', 'THURSDAY', 'FRIDAY',
        'SATURDAY'
    ]
    PERIODS = ['1d', '7d', '30d', '1w', '1m', '3m', '6m', '1y', 'max']

    RESOURCE_LIST = [
        'body',
        'activities',
        'foods/log',
        'foods/log/water',
        'sleep',
        'heart',
        'bp',
        'glucose',
    ]

    def __init__(self,
                 client_id,
                 client_secret,
                 access_token=None,
                 refresh_token=None,
                 expires_at=None,
                 refresh_cb=None,
                 redirect_uri=None,
                 system=JP,
                 **kwargs):
        """
        Fitbit(<id>, <secret>, access_token=<token>, refresh_token=<token>)
        """
        self.system = system
        self.client = FitbitOauth2Client(client_id,
                                         client_secret,
                                         access_token=access_token,
                                         refresh_token=refresh_token,
                                         expires_at=expires_at,
                                         refresh_cb=refresh_cb,
                                         redirect_uri=redirect_uri,
                                         **kwargs)

        # All of these use the same patterns, define the method for accessing
        # creating and deleting records once, and use curry to make individual
        # Methods for each
        for resource in Fitbit.RESOURCE_LIST:
            underscore_resource = resource.replace('/', '_')
            setattr(self, underscore_resource,
                    curry(self._COLLECTION_RESOURCE, resource))

            if resource not in ['body', 'glucose']:
                # Body and Glucose entries are not currently able to be deleted
                setattr(self, 'delete_%s' % underscore_resource,
                        curry(self._DELETE_COLLECTION_RESOURCE, resource))

    def make_request(self, *args, **kwargs):
        # This should handle data level errors, improper requests, and bad
        # serialization
        headers = kwargs.get('headers', {})
        headers.update({'Accept-Language': self.system})
        kwargs['headers'] = headers

        method = kwargs.get('method', 'POST' if 'data' in kwargs else 'GET')
        response = self.client.make_request(*args, **kwargs)

        if response.status_code == 202:
            return True
        if method == 'DELETE':
            if response.status_code == 204:
                return True
            else:
                raise exceptions.DeleteError(response)
        try:
            rep = json.loads(response.content.decode('utf8'))
        except ValueError:
            raise exceptions.BadResponse

        return rep

    def _get_common_args(self, user_id=None):
        common_args = (
            self.API_ENDPOINT,
            self.API_VERSION,
        )
        if not user_id:
            user_id = '-'
        common_args += (user_id, )
        return common_args

    def _get_date_string(self, date):
        if not isinstance(date, str):
            return date.strftime('%Y-%m-%d')
        return date

    def _COLLECTION_RESOURCE(self,
                             resource,
                             date=None,
                             user_id=None,
                             data=None):
        """
        Retrieving and logging of each type of collection data.

        Arguments:
            resource, defined automatically via curry
            [date] defaults to today
            [user_id] defaults to current logged in user
            [data] optional, include for creating a record, exclude for access

        This implements the following methods::

            body(date=None, user_id=None, data=None)
            activities(date=None, user_id=None, data=None)
            foods_log(date=None, user_id=None, data=None)
            foods_log_water(date=None, user_id=None, data=None)
            sleep(date=None, user_id=None, data=None)
            heart(date=None, user_id=None, data=None)
            bp(date=None, user_id=None, data=None)

        * https://dev.fitbit.com/docs/
        """

        if not date:
            date = datetime.date.today()
        date_string = self._get_date_string(date)

        kwargs = {'resource': resource, 'date': date_string}
        if not data:
            base_url = "{0}/{1}/user/{2}/{resource}/date/{date}.json"
        else:
            data['date'] = date_string
            base_url = "{0}/{1}/user/{2}/{resource}.json"
        url = base_url.format(*self._get_common_args(user_id), **kwargs)
        return self.make_request(url, data)

    def _DELETE_COLLECTION_RESOURCE(self, resource, log_id):
        """
        deleting each type of collection data

        Arguments:
            resource, defined automatically via curry
            log_id, required, log entry to delete

        This builds the following methods::

            delete_body(log_id)
            delete_activities(log_id)
            delete_foods_log(log_id)
            delete_foods_log_water(log_id)
            delete_sleep(log_id)
            delete_heart(log_id)
            delete_bp(log_id)

        """
        url = "{0}/{1}/user/-/{resource}/{log_id}.json".format(
            *self._get_common_args(), resource=resource, log_id=log_id)
        response = self.make_request(url, method='DELETE')
        return response

    def _resource_goal(self, resource, data={}, period=None):
        """ Handles GETting and POSTing resource goals of all types """
        url = "{0}/{1}/user/-/{resource}/goal{postfix}.json".format(
            *self._get_common_args(),
            resource=resource,
            postfix=('s/' + period) if period else '')
        return self.make_request(url, data=data)

    def _filter_nones(self, data):
        filter_nones = lambda item: item[1] is not None  # noqa
        filtered_kwargs = list(filter(filter_nones, data.items()))
        return {} if not filtered_kwargs else dict(filtered_kwargs)

    def get_bodyweight(self, base_date=None, user_id=None, end_date=None):
        return self._get_body('weight', base_date, user_id, end_date)

    def _get_body(self, type_, base_date=None, user_id=None, end_date=None):
        if not base_date:
            base_date = datetime.date.today()

        base_date_string = self._get_date_string(base_date)

        kwargs = {'type_': type_}
        base_url = "{0}/{1}/user/{2}/body/log/{type_}/date/{date_string}.json"

        if end_date:
            end_string = self._get_date_string(end_date)
            kwargs['date_string'] = '/'.join([base_date_string, end_string])
        else:
            kwargs['date_string'] = base_date_string

        url = base_url.format(*self._get_common_args(user_id), **kwargs)
        return self.make_request(url)
