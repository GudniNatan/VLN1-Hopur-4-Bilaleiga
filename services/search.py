from repositories.car_repository import CarRepository
from repositories.rent_order_repository import RentOrderRepository
from services.validate import Validate
from datetime import datetime, date


class Search(object):
    def search_cars(
            self, license_plate_number="", category="",
            is_automatic="", hide_available="", hide_unavailable="",
            availability_lower_bound=None, availability_upper_bound=None
            ):
        is_automatic = self.__process_yes_no_answer(is_automatic)
        hide_available = self.__process_yes_no_answer(hide_available)
        hide_unavailable = self.__process_yes_no_answer(hide_unavailable)
        if not (availability_lower_bound and availability_upper_bound):
            availability_lower_bound = datetime.now()
            availability_upper_bound = datetime.now()
        cars = CarRepository().get_all()
        relevant_cars = list()
        for car in cars:
            car_available = self.car_available(car, availability_lower_bound,
                                               availability_upper_bound)
            if is_automatic is not None:
                if is_automatic != car.get_automatic_transmission():
                    continue
            if hide_available is not None:
                if hide_available and car_available:
                    continue
            if hide_unavailable is not None:
                if hide_unavailable and not car_available:
                    continue
            if license_plate_number:
                if license_plate_number != car.get_license_plate_number:
                    continue
            if category:
                if category != car.get_category():
                    continue
            relevant_cars.append(car)
        return relevant_cars

    def __process_yes_no_answer(self, yes_no):
        if yes_no:
            yes_no = str(yes_no)[0].upper()
            if yes_no in ["J", "Y"]:
                return True
            return False

    def car_available(self, car, lower_time_bound, upper_time_bound=None):
        if upper_time_bound is None:
            upper_time_bound = lower_time_bound
        rent_orders = RentOrderRepository().get_all()
        for order in rent_orders:
            if order.get_pickup_time() <= upper_time_bound:
                if order.get_estimated_return_time() < lower_time_bound:
                    return False
        return True

    def search_rent_orders(self, number="", car="",
                           customer="", over_date=None):
        rent_orders = RentOrderRepository().get_all()
        matching_orders = list()
        for order in rent_orders:
            if number and number != str(order.get_order_number()):
                continue
            if car and car != str(car.get_license_plate_number()):
                continue
            if customer and customer != str(customer.get_driver_license_id()):
                continue
            if over_date:
                if type(over_date) not in [datetime, date]:
                    over_date = Validate().validate_datetime(over_date, "")
                if rent_orders.get_pickup_time() >= over_date:
                    continue
                if 