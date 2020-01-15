# -*- coding: utf-8 -*-
from .client import Fitbit
import pprint as pp
# import pandas as pd

# RAWDATA_PATH = "rawdata/activities.csv"


def get_activities():
    client = Fitbit()
    activities = client.get_activities("2020-01-01", "2020-01-15")
    # df = pd.DataFrame(activities)
    # df.to_csv(RAWDATA_PATH, index=None)

    pp.pprint(activities)


if __name__ == '__main__':
    get_activities()
