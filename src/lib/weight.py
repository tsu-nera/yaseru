# -*- coding: utf-8 -*-
from client import Fitbit


# poundで取得されるのでkgに変換
def pound_to_kg(pound):
    kg = pound * 0.454
    return kg


client = Fitbit()

# 31日分しか取得できない
# formatは yyyy-MM-dd
START_DATE = "2020-01-01"
END_DATE = "2020-01-11"

weights = client.get_weights(START_DATE, END_DATE)
print(weights)

# weight = bodyweights["weight"][0]["weight"]
# print(pound_to_kg(weight), "kg")
