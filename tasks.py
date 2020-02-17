from invoke import task
import pprint as pp

from src.utils.daily import get_daily, merge_daily
import src.lib.weight as weight
import src.lib.calory as calory
from src.lib.healthplanet import HealthPlanet


@task
def get_weights(c, base_date, end_date):
    weight.get_weights(base_date, end_date)


@task
def get_calories(c, base_date, end_date):
    calory.get_calories(base_date, end_date)


@task
def get_hp(c, days):
    hp = HealthPlanet()
    response = hp.get_innerscan(int(days))

    pp.pprint(response)


@task
def daily(c, year, month, day):
    get_daily(year, month, day)


@task
def daily_today(c):
    get_daily()


@task
def merge(c):
    merge_daily()
