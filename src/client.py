import datetime
import pandas as pd

import src.lib.weight as weight
import src.lib.calory as calory

DAILY_RAWDATA_PATH = "rawdata/daily.csv"


def get_daily_data(year, month, day):

    if not (year and month and day):
        target_date = datetime.datetime.now().strftime("%Y-%m-%d")
    else:
        target_date = "{}-{}-{}".format(year, month, day)

    df_weight = pd.DataFrame(weight.get_weights(target_date, target_date))
    df_calory = pd.DataFrame(calory.get_calories(target_date, target_date))

    df = pd.merge(df_weight, df_calory, how='outer', on="date")
    df.to_csv(DAILY_RAWDATA_PATH, index=False)