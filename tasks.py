import invoke

import src.client as client
import src.lib.weight as weight
import src.lib.calory as calory


@invoke.task
def get_weights(c, base_date, end_date):
    weight.get_weights(base_date, end_date)


@invoke.task
def get_calories(c, base_date, end_date):
    calory.get_calories(base_date, end_date)


@invoke.task
def get_daily(c, year, month, day):
    client.get_daily_data(year, month, day)