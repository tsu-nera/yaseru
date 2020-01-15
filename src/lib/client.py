import fitbit
from ast import literal_eval

import sys
sys.path.append('../src')

import src.env as env  # noqa

TOKEN_FILE = "src/token.txt"

tokens = open(TOKEN_FILE).read()
token_dict = literal_eval(tokens)
access_token = token_dict['access_token']
refresh_token = token_dict['refresh_token']


class Fitbit():
    def __init__(self, *args, **kwargs):
        self.client = fitbit.Fitbit(env.FITBIT_CLIENT_ID,
                                    env.FITBIT_CLIENT_SECRET,
                                    access_token=access_token,
                                    refresh_token=refresh_token,
                                    refresh_cb=self.updateToken)

    def updateToken(self, token):
        f = open(TOKEN_FILE, 'w')
        f.write(str(token))
        f.close()
        return

    def get_weights(self, start_date, end_date):
        weights = self.client.get_bodyweight(base_date=start_date,
                                             end_date=end_date)["weight"]

        def pound_to_kg(pound):
            kg = pound * 0.454
            return round(kg, 1)

        def convert(weight):
            return {
                "date": weight["date"],
                "weight": pound_to_kg(weight["weight"]),
                "bmi": weight["bmi"]
            }

        return [convert(weight) for weight in weights]
