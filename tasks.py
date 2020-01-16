import invoke

import src.client as client
import src.lib.weight as weight
import src.lib.calory as calory

import pandas as pd


@invoke.task
def get_weights(c, base_date, end_date):
    weight.get_weights(base_date, end_date)


@invoke.task
def get_calories(c, base_date, end_date):
    calory.get_calories(base_date, end_date)


@invoke.task
def get_daily(c, year, month, day):
    client.get_daily_data(year, month, day)


@invoke.task
def merge_daily_data(c):
    ALL_CALORIES_PATH = "data/all_calories.csv"
    ALL_WEIGHTS_PATH = "data/all_weights.csv"
    DAILY_RAWDATA_WEIGHT_PATH = "rawdata/daily_weight.csv"
    DAILY_RAWDATA_CALORY_PATH = "rawdata/daily_calory.csv"

    df_all_calories = pd.read_csv(ALL_CALORIES_PATH)
    df_all_weights = pd.read_csv(ALL_WEIGHTS_PATH)
    df_daily_calory = pd.read_csv(DAILY_RAWDATA_CALORY_PATH)
    df_daily_weight = pd.read_csv(DAILY_RAWDATA_WEIGHT_PATH)

    def merge_to_master(df_master, df_daily):
        return pd.concat([df_master,
                          df_daily]).drop_duplicates().sort_values("date")

    df_all_weights = merge_to_master(df_all_weights, df_daily_weight)
    df_all_weights.to_csv(ALL_WEIGHTS_PATH, index=False)
    df_all_calories = merge_to_master(df_all_calories, df_daily_calory)
    df_all_calories.to_csv(ALL_CALORIES_PATH, index=False)
