import requests
import datetime
from datetime import datetime as dt

from src.env import HP_USER_ID, HP_USER_PASSWORD, HP_CLIENT_ID, HP_CLIENT_SECRET  # noqa

from bs4 import BeautifulSoup  # noqa

from src.constants.healthplanet import HP_HOST, HP_REDIRECT_URI, HP_DEFAULT_SCOPE
from src.constants.healthplanet import HP_DEFAULT_RESPONSE_TYPE, HP_DEFAULT_GRANT_TYPE

from src.constants.healthplanet import HP_TAG_WEIGHT, HP_TAG_NAME_WEIGHT, HP_TAG_BODY_FAT_PARCENTAGE
from src.constants.healthplanet import HP_TAG_NAME_BODY_FAT_PARCENTAGE
from src.constants.healthplanet import HP_TAG_MUSCLE_MASS, HP_TAG_NAME_MUSCLE_MASS
from src.constants.healthplanet import HP_TAG_VISCERAL_FAT_LEVEL, HP_TAG_NAME_VISCERAL_FAT_LEVEL
from src.constants.healthplanet import HP_TAG_BASAL_METABOLIC_RATE, HP_TAG_NAME_BASAL_METABOLIC_RATE
from src.constants.healthplanet import HP_TAG_BODY_AGE, HP_TAG_NAME_BODY_AGE
from src.constants.healthplanet import HP_TAG_ESTIMATED_BONE_MASS, HP_TAG_NAME_ESTIMATED_BONE_MASS

from src.constants.healthplanet import HP_TAG_DICT

# import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).parent.parent.parent))


class HealthPlanet():
    def __init__(self, *args, **kwargs):
        self.session = requests.Session()
        self.token = self._get_token()

    def _uri(self, path):
        return 'https://{0}{1}'.format(HP_HOST, path)

    def _auth(self):
        payload = {
            'client_id': HP_CLIENT_ID,
            'redirect_uri': HP_REDIRECT_URI,
            'scope': HP_DEFAULT_SCOPE,
            'response_type': HP_DEFAULT_RESPONSE_TYPE,
        }
        return self.session.get(self._uri('/oauth/auth'), params=payload)

    def _login(self, url):
        payload = {
            'loginId': HP_USER_ID,
            'passwd': HP_USER_PASSWORD,
            'send': 1,
            'url': url,
        }
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        return self.session.post(self._uri('/login_oauth.do'),
                                 data=payload,
                                 headers=headers)

    def _get_access_token(self, code):
        payload = {
            'client_id': HP_CLIENT_ID,
            'client_secret': HP_CLIENT_SECRET,
            'redirect_uri': HP_REDIRECT_URI,
            'code': code,
            'grant_type': HP_DEFAULT_GRANT_TYPE,
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

    def _create_tags(self):
        tag_list = [
            HP_TAG_WEIGHT, HP_TAG_BODY_FAT_PARCENTAGE, HP_TAG_MUSCLE_MASS,
            HP_TAG_VISCERAL_FAT_LEVEL, HP_TAG_BASAL_METABOLIC_RATE,
            HP_TAG_BODY_AGE, HP_TAG_ESTIMATED_BONE_MASS
        ]
        return ','.join(map(str, tag_list))

    def _innerscan_formatter(self, input):
        data = input['data']

        output_dict = {}

        for d in data:
            date = d['date']
            value = d['keydata']
            tag = int(d['tag'])

            tag_name = HP_TAG_DICT[tag]

            if date in output_dict.keys():
                tmp = output_dict[date]
                tmp[tag_name] = value
                output_dict[date] = tmp
            else:
                output_dict[date] = {tag_name: value}

        output_list = []
        for k, v in output_dict.items():
            v['date'] = dt.strptime(k, '%Y%m%d%H%M%S')
            output_list.append(v)

            v[HP_TAG_NAME_BASAL_METABOLIC_RATE] = int(
                v[HP_TAG_NAME_BASAL_METABOLIC_RATE])
            v[HP_TAG_NAME_BODY_AGE] = int(v[HP_TAG_NAME_BODY_AGE])
            v[HP_TAG_NAME_BODY_FAT_PARCENTAGE] = float(
                v[HP_TAG_NAME_BODY_FAT_PARCENTAGE])
            v[HP_TAG_NAME_MUSCLE_MASS] = float(v[HP_TAG_NAME_MUSCLE_MASS])
            v[HP_TAG_NAME_ESTIMATED_BONE_MASS] = float(
                v[HP_TAG_NAME_ESTIMATED_BONE_MASS])
            v[HP_TAG_NAME_VISCERAL_FAT_LEVEL] = float(
                v[HP_TAG_NAME_VISCERAL_FAT_LEVEL])
            v[HP_TAG_NAME_WEIGHT] = float(v[HP_TAG_NAME_WEIGHT])

        return output_list

    def get_innerscan(self, past_days=7):
        from_date = dt.now() - datetime.timedelta(days=past_days)
        from_str = from_date.strftime('%Y%m%d%H%M%S')
        tags = self._create_tags()
        payload = {
            'access_token': self.token,
            'date': 1,
            'tag': tags,
            'from': from_str,
        }

        response = requests.get(self._uri('/status/innerscan.json'),
                                params=payload)

        return self._innerscan_formatter(response.json())
