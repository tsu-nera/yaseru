# -*- coding: utf-8 -*-
from .client import Fitbit
import pprint as pp
import pandas as pd

RAWDATA_PATH = "rawdata/calories.csv"


def get_calories():
    client = Fitbit()
    calories = client.get_calories("2019-12-01", "2019-12-31")
    df = pd.DataFrame(calories)
    df.to_csv(RAWDATA_PATH, index=None)

    pp.pprint(calories)


if __name__ == '__main__':
    get_calories()
