import datetime
import pandas as pd

from src.lib.weight import Weight
from src.lib.calory import Calory

DAILY_RAWDATA_WEIGHT_PATH = "rawdata/daily_weight.csv"
DAILY_RAWDATA_CALORY_PATH = "rawdata/daily_calory.csv"


def get_daily(year=None, month=None, day=None):

    if not (year and month and day):
        target_date = datetime.datetime.now().strftime("%Y-%m-%d")
    else:
        target_date = "{}-{}-{}".format(year, month.zfill(2), day.zfill(2))

    weight = Weight()
    calory = Calory()

    weight.get_to_csv(DAILY_RAWDATA_WEIGHT_PATH, target_date, target_date)
    calory.get_to_csv(DAILY_RAWDATA_CALORY_PATH, target_date, target_date)
