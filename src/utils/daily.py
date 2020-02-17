import datetime
import pandas as pd
import os

from src.lib.weight import Weight
from src.lib.calory import Calory
from src.lib.health_planet import HealthPlanet

RAWDATA_DIR = "rawdata"

DAILY_RAWDATA_WEIGHT_PATH = RAWDATA_DIR + "/daily_weight.csv"
DAILY_RAWDATA_CALORY_PATH = RAWDATA_DIR + "/daily_calory.csv"
DAILY_RAWDATA_HEALTHPLANET_PATH = RAWDATA_DIR + "/daily_healthplanet.csv"

ALL_CALORIES_PATH = "data/all_calories.csv"
ALL_WEIGHTS_PATH = "data/all_weights.csv"
ALL_HEALTHPLANETS_PATH = "data/all_healthplanets.csv"


def get_daily(year=None, month=None, day=None):
    weight = Weight()
    calory = Calory()
    hp = HealthPlanet()

    target_day = datetime.date(year, month, day)
    target_day_end = datetime.date(year, month,
                                   day) + datetime.timedelta(days=1)

    # from Health Planet
    hp.get_to_csv(DAILY_RAWDATA_HEALTHPLANET_PATH, target_day, target_day_end)
    for data in hp.data:
        weight.post(data['weight'], data['date'], data['body_fat_parcentage'])

    # from Fitbit
    weight.get_to_csv(DAILY_RAWDATA_WEIGHT_PATH, target_day, target_day)
    calory.get_to_csv(DAILY_RAWDATA_CALORY_PATH, target_day, target_day)

    weight.display()
    calory.display()
    hp.display()


def merge_daily():
    def _merge_to_master(df_master, df_daily):
        return pd.concat([df_master,
                          df_daily]).drop_duplicates().sort_values("date")

    def _is_valid_file(path):
        return os.path.exists(path) and os.path.getsize(path) > 1

    def _merge(all_data_path, target_data_path):
        if not _is_valid_file(all_data_path) or not _is_valid_file(
                target_data_path):
            return

        df_all = pd.read_csv(all_data_path)
        df_target = pd.read_csv(target_data_path)

        df_all = _merge_to_master(df_all, df_target)
        df_all.to_csv(all_data_path, index=False)

    _merge(ALL_CALORIES_PATH, DAILY_RAWDATA_CALORY_PATH)
    _merge(ALL_WEIGHTS_PATH, DAILY_RAWDATA_WEIGHT_PATH)
    _merge(ALL_HEALTHPLANETS_PATH, DAILY_RAWDATA_HEALTHPLANET_PATH)
