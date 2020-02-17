from abc import ABCMeta, abstractmethod

import pandas as pd
import pprint as pp

import datetime
from datetime import datetime as dt

import copy


class Base(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        self.data = None

    @abstractmethod
    def get(self, base_date=None, end_date=None):
        pass

    def get_pastdays(self, days=7):
        from_date = dt.now() - datetime.timedelta(days=days)
        to_date = dt.now()

        self.get(from_date, to_date)

    def get_pastdays_to_csv(self, path, days=7):
        self.get_pastdays(days)

        if len(self.data) != 0:
            self.to_csv(path)

    def to_csv(self, path):
        index = []
        values = []
        data = copy.deepcopy(self.data)

        for d in data:
            index.append(d.pop('date'))
            values.append(d)

        df = pd.DataFrame(values, index=index)
        df.index.name = 'date'
        df.to_csv(path, index=True)

    def get_to_csv(self, path, base_date=None, end_date=None):
        self.get(base_date, end_date)

        if len(self.data) != 0:
            self.to_csv(path)

    def display(self):
        pp.pprint(self.data)
