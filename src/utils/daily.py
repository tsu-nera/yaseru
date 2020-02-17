import datetime
import pandas as pd

from src.lib.weight import Weight
from src.lib.calory import Calory

DAILY_RAWDATA_WEIGHT_PATH = "rawdata/daily_weight.csv"
DAILY_RAWDATA_CALORY_PATH = "rawdata/daily_calory.csv"
DAILY_RAWDATA_HEALTHPLANET_PATH = "rawdata/daily_healthplanet.csv"

ALL_CALORIES_PATH = "data/all_calories.csv"
ALL_WEIGHTS_PATH = "data/all_weights.csv"
ALL_HEALTHPLANETS_PATH = "data/all_healthplanets.csv"


def get_daily(year=None, month=None, day=None):

    if not (year and month and day):
        target_date = datetime.datetime.now().strftime("%Y-%m-%d")
    else:
        target_date = "{}-{}-{}".format(year, month.zfill(2), day.zfill(2))

    weight = Weight()
    calory = Calory()

    weight.get_to_csv(DAILY_RAWDATA_WEIGHT_PATH, target_date, target_date)
    calory.get_to_csv(DAILY_RAWDATA_CALORY_PATH, target_date, target_date)


def merge_daily():
    df_all_calories = pd.read_csv(ALL_CALORIES_PATH)
    df_all_weights = pd.read_csv(ALL_WEIGHTS_PATH)
    #     df_all_hps = pd.read_csv(ALL_HEALTHPLANETS_PATH)

    df_daily_calory = pd.read_csv(DAILY_RAWDATA_CALORY_PATH)
    df_daily_weight = pd.read_csv(DAILY_RAWDATA_WEIGHT_PATH)

    #    df_daily_hp = pd.read_csv(DAILY_RAWDATA_HEALTHPLANET_PATH)

    def _merge_to_master(df_master, df_daily):
        return pd.concat([df_master,
                          df_daily]).drop_duplicates().sort_values("date")

    df_all_weights = _merge_to_master(df_all_weights, df_daily_weight)
    df_all_weights.to_csv(ALL_WEIGHTS_PATH, index=False)

    df_all_calories = _merge_to_master(df_all_calories, df_daily_calory)
    df_all_calories.to_csv(ALL_CALORIES_PATH, index=False)

    # df_all_hps = _merge_to_master(df_all_hps, df_daily_hp)
    # df_all_hps.to_csv(ALL_HEALTHPLANETS_PATH, index=False)
