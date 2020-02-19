import datetime
import pandas as pd
import os

from src.lib.weight import Weight
from src.lib.calory import Calory
from src.lib.health_planet import HealthPlanet

from src.constants.common import DAILY_RAWDATA_WEIGHT_PATH, DAILY_RAWDATA_CALORY_PATH, DAILY_RAWDATA_HEALTHPLANET_PATH
from src.constants.common import ALL_CALORIES_PATH, ALL_WEIGHTS_PATH, ALL_HEALTHPLANETS_PATH


def get_daily(year=None, month=None, day=None):
    weight = Weight()
    calory = Calory()
    hp = HealthPlanet()

    if year and month and day:
        base_datetime = datetime.datetime(year, month, day, 0, 0, 0)
        end_datetime = datetime.datetime(year, month, day, 23, 59, 59)
    else:
        now = datetime.datetime.now()
        base_datetime = datetime.datetime(now.year, now.month, now.day, 0, 0,
                                          0)
        end_datetime = datetime.datetime(now.year, now.month, now.day, 23, 59,
                                         59)

    # from Health Planet
    hp.get_to_csv(DAILY_RAWDATA_HEALTHPLANET_PATH, base_datetime, end_datetime)
    for data in hp.data:
        weight.post(data['weight'], data['date'], data['body_fat_parcentage'])

    # from Fitbit
    weight.get_to_csv(DAILY_RAWDATA_WEIGHT_PATH, base_datetime, end_datetime)
    calory.get_to_csv(DAILY_RAWDATA_CALORY_PATH, base_datetime, end_datetime)

    weight.display()
    calory.display()
    hp.display()


def merge_daily():
    def _merge_to_master(df_master, df_daily):
        return pd.concat([df_master, df_daily], sort=False).drop_duplicates(
            subset=["date", "weight"]).sort_values("date")

    def _merge_to_master_for_calory(df_master, df_daily):
        return pd.concat(
            [df_master, df_daily],
            sort=False).drop_duplicates(subset=["date"]).sort_values("date")

    def _is_valid_file(path):
        return os.path.exists(path) and os.path.getsize(path) > 1

    def _merge(all_data_path, target_data_path):
        if not _is_valid_file(all_data_path) or not _is_valid_file(
                target_data_path):
            return

        df_all = pd.read_csv(all_data_path)
        df_target = pd.read_csv(target_data_path)

        if "calories" in all_data_path:
            df_all = _merge_to_master_for_calory(df_all, df_target)
        else:
            df_all = _merge_to_master(df_all, df_target)

        df_all.to_csv(all_data_path, index=False)

    _merge(ALL_CALORIES_PATH, DAILY_RAWDATA_CALORY_PATH)
    _merge(ALL_WEIGHTS_PATH, DAILY_RAWDATA_WEIGHT_PATH)
    _merge(ALL_HEALTHPLANETS_PATH, DAILY_RAWDATA_HEALTHPLANET_PATH)
