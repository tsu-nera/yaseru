import fitbit
import env as env
from ast import literal_eval

TOKEN_FILE = "token.txt"

tokens = open(TOKEN_FILE).read()
token_dict = literal_eval(tokens)
access_token = token_dict['access_token']
refresh_token = token_dict['refresh_token']


def updateToken(token):
    f = open(TOKEN_FILE, 'w')
    f.write(str(token))
    f.close()
    return


client = fitbit.Fitbit(env.FITBIT_CLIENT_ID,
                       env.FITBIT_CLIENT_SECRET,
                       access_token=access_token,
                       refresh_token=refresh_token,
                       refresh_cb=updateToken)

TODAY = "2020-01-10"
bodyweights = client.get_bodyweight(base_date=TODAY)

print(bodyweights)

# weight = bodyweight["weight"][0]["weight"]
# print(pound_to_kg(weight), "kg")
