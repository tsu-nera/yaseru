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


def uri(path):
    return 'https://{0}{1}'.format(HOST, path)


def login(session, login_id, password, url):
    payload = {
        'loginId': login_id,
        'passwd': password,
        'send': 1,
        'url': url,
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    return session.post(uri('/login_oauth.do'), data=payload, headers=headers)


def auth(session):
    payload = {
        'client_id': HEALTHPLANET_CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': DEFAULT_SCOPE,
        'response_type': DEFAULT_RESPONSE_TYPE,
    }
    return session.get(uri('/oauth/auth'), params=payload)


def get_token(code):
    payload = {
        'client_id': HEALTHPLANET_CLIENT_ID,
        'client_secret': HEALTHPLANET_CLIENT_SECRET,
        'redirect_uri': REDIRECT_URI,
        'code': code,
        'grant_type': DEFAULT_GRANT_TYPE,
    }
    return requests.post(uri('/oauth/token'), params=payload)


def get_oauth_token(text):
    soup = BeautifulSoup(text, 'html.parser')
    value = soup.find('input', {'name': 'oauth_token'}).get('value')
    return value


def approval(session, token):
    payload = {
        'approval': True,
        'oauth_token': token,
    }
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    return session.post(uri('/oauth/approval.do'),
                        data=payload,
                        headers=headers)


def get_code(url):
    return url.split('code=')[1]


def get_innerscan(token, from_date):
    from_str = from_date.strftime('%Y%m%d%H%M%S')
    payload = {
        'access_token': token,
        'date': 1,
        'tag': '6021,6022',
        'from': from_str,
    }
    return requests.get(uri('/status/innerscan.json'), params=payload)


def get_data():
    session = requests.Session()
    auth_response = auth(session)
    login_response = login(session, HEALTHPLANET_USER_ID,
                           HEALTHPLANET_USER_PASSWORD, auth_response.url)
    token = get_oauth_token(login_response.text)
    approve_response = approval(session, token)
    code = get_code(approve_response.url)
    token_response = get_token(code)
    access_token = token_response.json()['access_token']
    innerscan_response = get_innerscan(
        access_token,
        dt.now() - datetime.timedelta(days=SCOPE_DAYS))
    return innerscan_response.json()


print(get_data())
