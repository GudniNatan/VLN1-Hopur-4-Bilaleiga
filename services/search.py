from repositories.car_repository import CarRepository
from repositories.rent_order_repository import RentOrderRepository
from services.validation import Validation
from datetime import datetime, date
from services.utils import Utils


class Search(object):
    def search_cars(
            self, license_plate="", category="", seat_count=0,
            is_automatic="", hide_available="", hide_unavailable="",
            availability_lower_bound=None, availability_upper_bound=None,
            in_branch=None
            ):
        process_yes_no_answer = Utils().process_yes_no_answer
        is_automatic = process_yes_no_answer(is_automatic)
        hide_available = process_yes_no_answer(hide_available)
        hide_unavailable = process_yes_no_answer(hide_unavailable)
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
            if seat_count and seat_count != str(car.get_seat_count()):
                continue
            if car.get_license_plate_number().count(license_plate) == 0:
                continue
            if category:
                if category != car.get_category():
                    continue
            if in_branch:
                if str(in_branch) != str(car.get_current_branch()):
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
        if type(lower_time_bound) not in [datetime, date]:
            lower_time_bound = Validation().validate_datetime(lower_time_bound)
        if type(upper_time_bound) not in [datetime, date]:
            upper_time_bound = lower_time_bound
        rent_orders = RentOrderRepository().get_all()
        for order in rent_orders:
            if order.get_pickup_time() <= upper_time_bound:
                if order.get_estimated_return_time() >= lower_time_bound:
                    return False
        return True

    def __order_active(self, order):
        if order.get_pickup_time() <= datetime.now():
            if order.get_return_time() is None:
                return True
        return False

    def search_rent_orders(self, number="", customer="",
                           car="", active: bool = None):
        rent_orders = RentOrderRepository().get_all()
        matching_orders = list()
        for order in rent_orders:
            if number and number != str(order.get_order_number()):
                continue
            if str(order.get_order_number()).count(number) == 0:
                continue
            if order.get_car().get_key().count(car) == 0:
                continue
            if customer and customer != str(order.get_customer().get_key()):
                continue
            if order.get_customer().get_key().count(customer) == 0:
                continue
            if (not self.__order_active(order)) == active:
                continue
            matching_orders.append(order)
        return matching_orders
