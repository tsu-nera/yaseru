import requests
import datetime
from datetime import datetime as dt

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.env import HEALTHPLANET_CLIENT_ID, HEALTHPLANET_CLIENT_SECRET  # noqa
from src.env import HEALTHPLANET_USER_ID, HEALTHPLANET_USER_PASSWORD  # noqa

from bs4 import BeautifulSoup  # noqa

HOST = 'www.healthplanet.jp'
REDIRECT_URI = 'https://www.healthplanet.jp/success.html'
DEFAULT_SCOPE = 'innerscan'
DEFAULT_RESPONSE_TYPE = 'code'
DEFAULT_GRANT_TYPE = 'authorization_code'
SCOPE_DAYS = 1


class HealthPlanet():
    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.token = self._get_token()

    def _uri(self, path):
        return 'https://{0}{1}'.format(HOST, path)

    def _auth(self):
        payload = {
            'client_id': HEALTHPLANET_CLIENT_ID,
            'redirect_uri': REDIRECT_URI,
            'scope': DEFAULT_SCOPE,
            'response_type': DEFAULT_RESPONSE_TYPE,
        }
        return self.session.get(self._uri('/oauth/auth'), params=payload)

    def _login(self, url):
        payload = {
            'loginId': HEALTHPLANET_USER_ID,
            'passwd': HEALTHPLANET_USER_PASSWORD,
            'send': 1,
            'url': url,
        }
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        return self.session.post(self._uri('/login_oauth.do'),
                                 data=payload,
                                 headers=headers)

    def _get_access_token(self, code):
        payload = {
            'client_id': HEALTHPLANET_CLIENT_ID,
            'client_secret': HEALTHPLANET_CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'code': code,
            'grant_type': DEFAULT_GRANT_TYPE,
        }
        return requests.post(self._uri('/oauth/token'), params=payload)

    def _get_oauth_token(self, text):
        soup = BeautifulSoup(text, 'html.parser')
        value = soup.find('input', {'name': 'oauth_token'}).get('value')
        return value

    def _approval(self, token):
        payload = {
            'approval': True,
            'oauth_token': token,
        }
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        return self.session.post(self._uri('/oauth/approval.do'),
                                 data=payload,
                                 headers=headers)

    def _get_code(self, url):
        return url.split('code=')[1]

    def _get_token(self):
        auth_response = self._auth()
        login_response = self._login(auth_response.url)
        token = self._get_oauth_token(login_response.text)
        approve_response = self._approval(token)
        code = self._get_code(approve_response.url)
        return self._get_access_token(code).json()['access_token']

    def get_innerscan(self):
        from_date = dt.now() - datetime.timedelta(days=SCOPE_DAYS)
        from_str = from_date.strftime('%Y%m%d%H%M%S')
        payload = {
            'access_token': self.token,
            'date': 1,
            'tag': '6021,6022',
            'from': from_str,
        }
        return requests.get(self._uri('/status/innerscan.json'),
                            params=payload).json()
