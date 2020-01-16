# -*- coding: utf-8 -*-
from .fitbit import Fitbit
from pprint import pprint as pp
import pandas as pd

RAWDATA_PATH = "rawdata/calories.csv"


def get_calories(base_date=None, end_date=None, debug=False):
    client = Fitbit()
    calories = client.get_calories(base_date, end_date)
    df = pd.DataFrame(calories)
    df.to_csv(RAWDATA_PATH, index=None)

    if debug:
        pp(calories)

    return calories


if __name__ == '__main__':
    get_calories(debug=True)
