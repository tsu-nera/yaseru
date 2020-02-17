# -*- coding: utf-8 -*-

from .base import Base
from .fitbit import Fitbit


class Weight(Base):
    def __init__(self, *args, **kwargs):
        self.client = Fitbit()

    def get(self, base_date=None, end_date=None):
        self.data = self.client.get_weights(base_date, end_date)

        return self.data
