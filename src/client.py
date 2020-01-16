import datetime
import pandas as pd

import src.lib.weight as weight
import src.lib.calory as calory

DAILY_RAWDATA_WEIGHT_PATH = "rawdata/daily_weight.csv"
DAILY_RAWDATA_CALORY_PATH = "rawdata/daily_calory.csv"


def get_daily_data(year, month, day):

    if not (year and month and day):
        target_date = datetime.datetime.now().strftime("%Y-%m-%d")
    else:
        target_date = "{}-{}-{}".format(year, month, day)

    df_weight = pd.DataFrame(weight.get_weights(target_date, target_date))
    df_calory = pd.DataFrame(calory.get_calories(target_date, target_date))

    df_weight.to_csv(DAILY_RAWDATA_WEIGHT_PATH, index=False)
    df_calory.to_csv(DAILY_RAWDATA_CALORY_PATH, index=False)
