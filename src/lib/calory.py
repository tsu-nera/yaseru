from .base import Base
from .fitbit import Fitbit


class Calory(Base):
    def __init__(self, *args, **kwargs):
        self.client = Fitbit()

    def date_format(self, datetime):
        return datetime.strftime("%Y-%m-%d")

    def get(self, base_datetime=None, end_datetime=None):

        base_date = self.date_format(base_datetime)
        end_date = self.date_format(end_datetime)

        self.data = self.client.get_calories(base_date, end_date)
        return self.data
