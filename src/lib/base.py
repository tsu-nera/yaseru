from abc import ABCMeta, abstractmethod

import pandas as pd
import pprint as pp


class Base(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        self.data = None
        self.rawdata_path = None

    @abstractmethod
    def get(self, base_date=None, end_date=None):
        pass

    def to_csv(self, path):
        df = pd.DataFrame(self.data)
        df.to_csv(path, index=None)

    def get_to_csv(self, path, base_date=None, end_date=None):
        self.get(base_date, end_date)
        self.to_csv(path)

    def display(self):
        pp.pprint(self.data)
