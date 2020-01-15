# -*- coding: utf-8 -*-
from .client import Fitbit
import pprint as pp


def get_weights():
    client = Fitbit()
    weights = client.get_weights("2020-01-01", "2020-01-11")
    pp.pprint(weights)


if __name__ == '__main__':
    get_weights()
