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

    def apply_converter(self, func, data):
        return [func(x) for x in data]

    def get_weights(self, start_date, end_date):
        weights = self.client.get_bodyweight(base_date=start_date,
                                             end_date=end_date)["weight"]

        def convert(weight):
            return {
                "date": weight["date"],
                "weight": weight["weight"],
                "bmi": weight["bmi"]
            }

        return self.apply_converter(convert, weights)

    def get_calories(self, start_date, end_date):
        calories = self.client.get_calories(
            base_date=start_date, end_date=end_date)["activities-calories"]
        calories_bmr = self.client.get_calories_bmr(
            base_date=start_date, end_date=end_date)["activities-caloriesBMR"]
        activity_calories = self.client.get_activity_calories(
            base_date=start_date,
            end_date=end_date)["activities-activityCalories"]
        calories_in = self.client.get_calories_in(
            base_date=start_date, end_date=end_date)["foods-log-caloriesIn"]

        print(calories_in)

        return [{
            "date": a["dateTime"],
            "calory": int(a["value"]),
            "calory_bmr": int(b["value"]),
            "calory_activity": c["value"],
            "calory_out": int(b["value"]) + int(c["value"]),
            "calory_in": int(d["value"])
        } for a, b, c, d in zip(calories, calories_bmr, activity_calories,
                                calories_in)]
