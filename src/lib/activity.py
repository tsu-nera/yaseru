# -*- coding: utf-8 -*-
from .client import Fitbit
import pprint as pp
# import pandas as pd

# RAWDATA_PATH = "rawdata/activities.csv"


def get_calories():
    client = Fitbit()
    calories = client.get_calories("2020-01-01", "2020-01-16")
    # df = pd.DataFrame(activities)
    # df.to_csv(RAWDATA_PATH, index=None)

    pp.pprint(calories)


if __name__ == '__main__':
    get_calories()
