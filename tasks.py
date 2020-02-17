from invoke import task

from src.utils.daily import get_daily, merge_daily
import src.lib.weight as weight
import src.lib.calory as calory
from src.lib.health_planet import HealthPlanet


@task
def get_weights(c, base_date, end_date):
    weight.get_weights(base_date, end_date)


@task
def get_calories(c, base_date, end_date):
    calory.get_calories(base_date, end_date)


@task
def get_hp(c, days):
    hp = HealthPlanet()
    hp.get_pastdays(int(days))
    hp.display()


@task
def daily(c, year, month, day):
    get_daily(int(year), int(month), int(day))


@task
def daily_today(c):
    get_daily()


@task
def merge(c):
    merge_daily()
