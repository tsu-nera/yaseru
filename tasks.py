from invoke import task

from src.utils.daily import get_daily, merge_daily
from src.lib.weight import Weight
from src.lib.health_planet import HealthPlanet


@task
def get_hp(c, days):
    hp = HealthPlanet()
    hp.get_pastdays(int(days))
    hp.display()


@task
def sync_hp_fitbit(c, days):
    hp = HealthPlanet()
    weight = Weight()
    hp.get_pastdays(int(days))

    for data in hp.data:
        print('{} - 体重{}kg/体脂肪率{}%'.format(data['date'], data['weight'],
                                           data['body_fat_parcentage']))
        weight.post(data['weight'], data['date'], data['body_fat_parcentage'])


@task
def daily(c, year, month, day):
    get_daily(int(year), int(month), int(day))


@task
def daily_today(c):
    get_daily()


@task
def merge(c):
    merge_daily()


@task
def post_weight(c, value):
    weight = Weight()
    weight.post(value=float(value))


@task
def post_weight_fat(c, value, fat):
    weight = Weight()
    weight.post(value=float(value), fat=float(fat))
