from repositories.car_repository import CarRepository
from repositories.customer_repository import CustomerRepository
from repositories.rent_order_repository import RentOrderRepository
from repositories.salesperson_repository import SalespersonRepository
from services.validation import Validation
from datetime import datetime, date
from services.utils import Utils

# This class contains a few different search funtions
# for use by controllers and validation


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
        license_plate = license_plate.strip().replace("-", "").upper()
        if type(hide_unavailable) != bool:
            hide_unavailable = process_yes_no_answer(hide_unavailable)
        if not (availability_lower_bound and availability_upper_bound):
            availability_lower_bound = datetime.now()
            availability_upper_bound = datetime.now()
        cars = CarRepository().get_all()
        relevant_cars = list()
        for car in cars:
            car_available = self.car_available(
                car, availability_lower_bound, availability_upper_bound
            )
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
            car_license_plate = car.get_key().replace("-", "").upper()
            if car_license_plate.count(license_plate) == 0:
                continue
            if type(category) == str:
                car_category = car.get_category()["category"].upper()
                if car_category.count(category.upper().strip()) == 0:
                    continue
            elif category:
                if category != car.get_category():
                    continue
            if in_branch:
                if str(in_branch) != str(car.get_current_branch()):
                    continue
            if in_branch and car.get_current_branch() != in_branch:
                continue
            relevant_cars.append(car)
        return relevant_cars

    def car_available(self, car, lower_time_bound, upper_time_bound=None):
        if type(lower_time_bound) not in [datetime, date]:
            lower_time_bound = Validation().validate_datetime(lower_time_bound)
        if type(upper_time_bound) not in [datetime, date]:
            upper_time_bound = lower_time_bound
        rent_orders = RentOrderRepository().get_all()
        for order in rent_orders:
            if order.get_car() != car:
                continue
            elif order.get_pickup_time() <= upper_time_bound:
                if order.get_estimated_return_time() >= lower_time_bound:
                    return False
        return True

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
            if (not Utils().order_active(order)) == active:
                continue
            matching_orders.append(order)
        return matching_orders

    def search_customers(self, driver_license_id="",
                         personal_id="", name=""):
        customers = CustomerRepository().get_all()
        driver_id = driver_license_id.strip().upper()
        personal_id = personal_id.strip().upper()
        name = name.strip()
        personal_id = personal_id.strip()
        for i in range(len(customers) - 1, -1, -1):
            person = customers[i]
            if person.get_driver_license_id().upper().count(driver_id) == 0:
                customers.pop(i)
            elif person.get_name().upper().count(name.upper()) == 0:
                customers.pop(i)
            elif person.get_personal_id().upper().count(personal_id) == 0:
                customers.pop(i)
        return customers

    def search_salespeople(self, username="", name="", email="", phone=""):
        salespeople = SalespersonRepository().get_all()
        username = username.strip()
        name = name.strip()
        email = email.strip()
        phone = phone.strip()
        for i in range(len(salespeople) - 1, -1, -1):
            person = salespeople[i]
            if username and username != person.get_username():
                salespeople.pop(i)
            elif name and name != person.get_name():
                salespeople.pop(i)
            elif email and email != person.get_email():
                salespeople.pop(i)
            elif phone and phone != person.get_phone():
                salespeople.pop(i)
        return salespeople
