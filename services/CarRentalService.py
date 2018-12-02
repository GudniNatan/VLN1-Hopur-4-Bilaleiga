from repositories.CarRepository import CarRepository
#from repositories.OrderRepository import OrderRepository
import datetime


class CarRentalService(object):
    def __init__(self):
        self.car_repository = CarRepository()
        #self.order_repository = OrderRepository()

    def validate_datetime(self, date_time_str_list):
        date_str, time_str = date_time_str_list
        try:
            time_format = "%Y-%m-%dT%H:%M"
            datetime_str = date_str + "T" + time_str
            return datetime.datetime.strptime(datetime_str, time_format)
        except ValueError:
            pass
        try:
            year_str, month_str, day_str = date_str.split("-")
        except ValueError:
            try:
                year_str, month_str, day_str = date_str.split("/")
            except ValueError:
                return None
        try:
            hour_str, minute_str = time_str.split(":")
        except ValueError:
            try:
                hour_str, minute_str = time_str.split("-")
            except ValueError:
                return None
        try:
            year = int(year_str)
            month = int(month_str)
            day = int(day_str)
            hour = int(hour_str)
            minute = int(minute_str)
            return datetime.datetime(year, month, day, hour, minute)
        except ValueError:
            return None

    def validate_return_datetime(self, pickup_datetime, date_time_str_list):
        return_datetime = self.validate_datetime(date_time_str_list)
        if return_datetime is not None:
            min_rent_period = datetime.timedelta(days=1)
            if return_datetime - pickup_datetime >= min_rent_period:
                return return_datetime

    def search_cars(self, pickup_datetime, return_datetime, category):
        '''Search for cars available during a given timeframe,
        of a given type'''
        cars = self.car_repository.get_all()
        orders = self.order_repository.get_all()

        for car in cars:
            if car.category == category:
                pass
