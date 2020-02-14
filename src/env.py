import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

FITBIT_CLIENT_ID = os.environ.get("FITBIT_CLIENT_ID")
FITBIT_CLIENT_SECRET = os.environ.get("FITBIT_CLIENT_SECRET")
FITBIT_ACCESS_TOKEN = os.environ.get("FITBIT_ACCESS_TOKEN")
FITBIT_REFRESH_TOKEN = os.environ.get("FITBIT_REFRESH_TOKEN")

HEALTHPLANET_CLIENT_ID = os.environ.get("HEALTHPLANET_CLIENT_ID")
HEALTHPLANET_CLIENT_SECRET = os.environ.get("HEALTHPLANET_CLIENT_SECRET")
HEALTHPLANET_USER_ID = os.environ.get("HEALTHPLANET_USER_ID")
HEALTHPLANET_USER_PASSWORD = os.environ.get("HEALTHPLANET_USER_PASSWORD")
