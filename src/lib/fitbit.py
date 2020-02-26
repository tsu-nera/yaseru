import fitbit
from ast import literal_eval

import sys
sys.path.append('../src')

import src.env as env  # noqa

TOKEN_FILE = "src/token.json"

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

    def apply_converter(self, func, data):
        return [func(x) for x in data]

    def _date_time(self, date, time):
        return "{} {}".format(date, time)

    def get_weights(self, base_date, end_date):
        weights = self.client.get_bodyweight(base_date=base_date,
                                             end_date=end_date)["weight"]
        weight_dict = {}
        for data in weights:
            datetime = self._date_time(data['date'], data['time'])
            weight_dict[datetime] = {
                'date': datetime,
                'weight': data['weight'],
                'bmi': data['bmi']
            }

        fats = self.client.get_bodyfat(base_date=base_date,
                                       end_date=end_date)['fat']

        fat_dict = {}
        for data in fats:
            datetime = self._date_time(data['date'], data['time'])
            fat_dict[datetime] = {'date': datetime, 'fat': data['fat']}

        for k, v in fat_dict.items():
            tmp = weight_dict[k]
            tmp['fat'] = v['fat']
            weight_dict[k] = tmp

        return list(weight_dict.values())

    def post_weight(self, weight, date, time=None, fat=None):
        self.client.post_bodyweight(weight=weight,
                                    date=date,
                                    time=time,
                                    fat=fat)

    def get_calories(self, base_date, end_date):
        calories = self.client.get_calories(
            base_date=base_date, end_date=end_date)["activities-calories"]
        calories_bmr = self.client.get_calories_bmr(
            base_date=base_date, end_date=end_date)["activities-caloriesBMR"]
        activity_calories = self.client.get_activity_calories(
            base_date=base_date,
            end_date=end_date)["activities-activityCalories"]
        calories_in = self.client.get_calories_in(
            base_date=base_date, end_date=end_date)["foods-log-caloriesIn"]

        return [{
            "date": "{} {}".format(a["dateTime"], "23:59:59"),
            "calory": int(a["value"]),
            "calory_bmr": int(b["value"]),
            "calory_activity": c["value"],
            "calory_out": int(b["value"]) + int(c["value"]),
            "calory_in": int(d["value"])
        } for a, b, c, d in zip(calories, calories_bmr, activity_calories,
                                calories_in)]

    def get_activities(self, base_date, end_date):
        activities = self.client.activities_list(base_date=base_date)

        print(activities)