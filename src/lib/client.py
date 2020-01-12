import fitbit
from ast import literal_eval

import env as env
TOKEN_FILE = "../token.txt"

tokens = open(TOKEN_FILE).read()
token_dict = literal_eval(tokens)
access_token = token_dict['access_token']
refresh_token = token_dict['refresh_token']


class Fitbit():
    def updateToken(self, token):
        f = open(TOKEN_FILE, 'w')
        f.write(str(token))
        f.close()
        return

    def create(self):
        return fitbit.Fitbit(env.FITBIT_CLIENT_ID,
                             env.FITBIT_CLIENT_SECRET,
                             access_token=access_token,
                             refresh_token=refresh_token,
                             refresh_cb=self.updateToken)
