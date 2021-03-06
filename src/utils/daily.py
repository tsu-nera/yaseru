import datetime
import pandas as pd
import os

from src.lib.weight import Weight
from src.lib.calory import Calory
from src.lib.health_planet import HealthPlanet
from src.lib.activity import Activity

from src.constants.common import DAILY_RAWDATA_WEIGHT_PATH, DAILY_RAWDATA_CALORY_PATH, DAILY_RAWDATA_HEALTHPLANET_PATH, DAILY_RAWDATA_ACTIVITY_PATH
from src.constants.common import ALL_CALORIES_PATH, ALL_WEIGHTS_PATH, ALL_HEALTHPLANETS_PATH, ALL_ACTIVITIES_PATH
from src.constants.bigquery import DATASET_ID, PROJECT_ID, DATASET_NAME


def get_daily(year=None, month=None, day=None):
    weight = Weight()
    calory = Calory()
    hp = HealthPlanet()
    activity = Activity()

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
    activity.get_to_csv(DAILY_RAWDATA_ACTIVITY_PATH, base_datetime,
                        end_datetime)

    weight.display()
    calory.display()
    hp.display()
    activity.display()


def _is_valid_file(path):
    return os.path.exists(path) and os.path.getsize(path) > 1


def _merge_to_master(df_master, df_daily):
    return pd.concat([df_master, df_daily], sort=False).drop_duplicates(
        subset=["date", "weight"]).sort_values("date")


def _merge_to_master2(df_master, df_daily):
    return pd.concat([df_master, df_daily], sort=False).drop_duplicates(
        subset=["date"], keep="last").sort_values("date")


def merge_daily():
    def _merge(all_data_path, target_data_path):
        if not _is_valid_file(all_data_path) or not _is_valid_file(
                target_data_path):
            return

        df_all = pd.read_csv(all_data_path)
        df_target = pd.read_csv(target_data_path)

        if "calories" or "activities" in all_data_path:
            df_all = _merge_to_master2(df_all, df_target)
        else:
            df_all = _merge_to_master(df_all, df_target)

        df_all.to_csv(all_data_path, index=False)

    _merge(ALL_CALORIES_PATH, DAILY_RAWDATA_CALORY_PATH)
    _merge(ALL_WEIGHTS_PATH, DAILY_RAWDATA_WEIGHT_PATH)
    _merge(ALL_HEALTHPLANETS_PATH, DAILY_RAWDATA_HEALTHPLANET_PATH)
    _merge(ALL_ACTIVITIES_PATH, DAILY_RAWDATA_ACTIVITY_PATH)


def upload_daily_to_bq():
    def _upload(table_name, target_data_path):
        if not _is_valid_file(target_data_path):
            return

        df_target = pd.read_csv(target_data_path)

        query = "SELECT * FROM {}.{};".format(DATASET_ID, table_name)
        df_bq = pd.read_gbq(query, dialect="standard")

        df_bq["date"] = df_bq["date"].apply(
            lambda x: x.strftime('%Y-%m-%d %H:%M:%S'))

        if "calory" or "activity" in target_data_path:
            df_bq = _merge_to_master2(df_bq, df_target)
        else:
            df_bq = _merge_to_master(df_bq, df_target)

        df_bq["date"] = df_bq["date"].apply(
            lambda x: datetime.datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
        df_bq.to_gbq(".".join([DATASET_NAME, table_name]),
                     PROJECT_ID,
                     if_exists="replace")

    _upload("calories", DAILY_RAWDATA_CALORY_PATH)
    _upload("weights", DAILY_RAWDATA_WEIGHT_PATH)
    _upload("healthplanets", DAILY_RAWDATA_HEALTHPLANET_PATH)
    _upload("activities", DAILY_RAWDATA_ACTIVITY_PATH)
