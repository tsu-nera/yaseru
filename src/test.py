import fitbit
import env as env

client = fitbit.Fitbit(env.FITBIT_CLIENT_ID,
                       env.FITBIT_CLIENT_SECRET,
                       access_token=env.FITBIT_ACCESS_TOKEN,
                       refresh_token=env.FITBIT_REFRESH_TOKEN)

result = client.sleep(date="2019-12-01")

print(result)
