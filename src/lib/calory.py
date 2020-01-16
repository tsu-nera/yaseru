# -*- coding: utf-8 -*-
from .client import Fitbit
import pprint as pp
import pandas as pd

RAWDATA_PATH = "rawdata/calories.csv"


def get_calories(base_date=None, end_date=None):
    client = Fitbit()
    calories = client.get_calories(base_date, end_date)
    df = pd.DataFrame(calories)
    df.to_csv(RAWDATA_PATH, index=None)

    pp.pprint(calories)


if __name__ == '__main__':
    get_calories()
