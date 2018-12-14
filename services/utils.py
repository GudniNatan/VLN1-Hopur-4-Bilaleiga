from datetime import datetime
from models.rent_order import RentOrder


class Utils(object):
    def process_yes_no_answer(self, yes_no):
            if yes_no:
                yes_no = str(yes_no)[0].upper()
                if yes_no in ["J", "Y"]:
                    return True
                return False

    def count_days_in_range(self, datetime_1, datetime_2):
        # This function counts the days in a range, and
        # acts as a ceiling function for partial days
        return abs((datetime_1 - datetime_2).days)

    def calculate_base_cost(self, car, pickup_datetime, return_datetime):
        days = self.count_days_in_range(pickup_datetime, return_datetime)
        day_cost = car.get_category()["price"]
        return days * day_cost

    def calculate_addon_cost(self, car):
        addon_price = RentOrder.ADDON_PRICE
        addon_count = len(car.get_extra_properties())
        return addon_price * addon_count

    def calculate_extra_cost(self, order):
        return []

    def order_active(self, order):
        if order.get_pickup_time() <= datetime.now():
            if order.get_return_time() is None:
                return True
        return False
