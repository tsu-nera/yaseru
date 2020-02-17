# -*- coding: utf-8 -*-

from .base import Base
from .fitbit import Fitbit
from datetime import datetime


class Weight(Base):
    def __init__(self, *args, **kwargs):
        self.client = Fitbit()

    def date_format(self, dt):
        return dt.strftime("%Y-%m-%d")

    def time_format(self, dt):
        return dt.strftime("%H:%M:%S")

    def get(self, base_datetime=None, end_datetime=None):
        base_date = self.date_format(base_datetime)
        end_date = self.date_format(end_datetime)

        self.data = self.client.get_weights(base_date, end_date)
        return self.data

    def post(self, value, dt=None, fat=None):
        if not dt:
            dt = datetime.now()
        date_str = self.date_format(dt)
        time_str = self.time_format(dt)

        self.client.post_weight(weight=value,
                                date=date_str,
                                time=time_str,
                                fat=fat)
