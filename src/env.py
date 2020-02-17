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

HP_CLIENT_ID = os.environ.get("HP_CLIENT_ID")
HP_CLIENT_SECRET = os.environ.get("HP_CLIENT_SECRET")
HP_USER_ID = os.environ.get("HP_USER_ID")
HP_USER_PASSWORD = os.environ.get("HP_USER_PASSWORD")
