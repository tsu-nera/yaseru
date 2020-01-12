# -*- coding: utf-8 -*-
from client import Fitbit
import pprint as pp

client = Fitbit()

weights = client.get_weights("2020-01-01", "2020-01-11")

pp.pprint(weights)
