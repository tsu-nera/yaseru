# -*- coding: utf-8 -*-
from .client import Fitbit
# import pprint as pp
import pandas as pd

RAWDATA_PATH = "rawdata/weights.csv"


def get_weights():
    client = Fitbit()
    weights = client.get_weights("2020-01-01", "2020-01-15")
    df = pd.DataFrame(weights)
    df.to_csv(RAWDATA_PATH, index=None)

    # pp.pprint(weights)


if __name__ == '__main__':
    get_weights()
