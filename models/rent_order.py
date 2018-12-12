from models.model import Model
from models.customer import Customer
from models.car import Car
from datetime import datetime


class RentOrder(Model):
    INSURANCE_PERCENT = 0.05
    KM_ALLOWANCE_PER_DAY = 100
    EXTRA_INSURANCE = 3000
    ADDON_PRICE = 450

    def __init__(
            self, order_number: int, car: Car, customer: Customer,
            pickup_time: datetime, estimated_return_time: datetime,
            pickup_branch_name: str, return_branch_name: str,
            include_extra_insurance: bool, base_cost: int,
            remaining_debt: int = -1, kilometers_driven: int = 0,
            return_time: datetime = None,
            ):
        self.__order_number = order_number
        self.__car = car
        self.__customer = customer
        self.__pickup_time = pickup_time
        self.__estimated_return_time = estimated_return_time
        self.__pickup_branch_name = pickup_branch_name
        self.__return_branch_name = return_branch_name
        self.__remaining_debt = remaining_debt
        self.__kilometers_driven = kilometers_driven
        self.__return_time = return_time
        self.__base_cost = base_cost
        self.__insurance_total = int(base_cost * self.INSURANCE_PERCENT)
        self.__extra_insurance_total = 0
        if include_extra_insurance:
            self.__extra_insurance_total += self.EXTRA_INSURANCE
        self.__total_cost = base_cost + self.__extra_insurance_total
        if remaining_debt == -1:
            self.__remaining_debt = self.__total_cost

    def csv_repr(self):
        rent_order_dict = self.get_dict()
        return_time_str = self.__estimated_return_time.isoformat()
        lpn = self.__customer.get_key()
        rent_order_dict["car"] = self.__car.get_license_plate_number()
        rent_order_dict["customer"] = lpn
        rent_order_dict["pickup_time"] = self.__pickup_time.isoformat()
        rent_order_dict["estimated_return_time"] = return_time_str
        if self.__return_time:
            rent_order_dict["return_time"] = self.__return_time.isoformat()
        return rent_order_dict

    def get_dict(self):
        return {
            "order_number": self.__order_number,
            "car": self.__car,
            "customer": self.__customer,
            "pickup_time": self.__pickup_time,
            "estimated_return_time": self.__estimated_return_time,
            "pickup_branch_name": self.__pickup_branch_name,
            "return_branch_name": self.__return_branch_name,
            "include_extra_insurance": self.__extra_insurance_total != 0,
            "base_cost": self.__base_cost,
            "remaining_debt": self.__remaining_debt,
            "kilometers_driven": self.__kilometers_driven,
            "return_time": self.__return_time,
        }

    def __str__(self):
        order_string = "Pöntun #{},\n\tViðskiptavinur: {},\n\tÖkuskírteini {},"
        order_string += "\n\tBíltegund {},\n\tBílnúmer {},\n\tKostnaður {}"
        return order_string.format(
            str(self.__order_number), self.get_customer().get_name(),
            self.__customer.get_driver_license_id(), self.__car.get_model(),
            self.__car.get_license_plate_number(), str(self.__total_cost)
        )

    def __eq__(self, other):
        if type(other) == type(self):
            return self.get_order_number() == other.get_order_number()
        else:
            return self.get_order_number() == str(other)

    # Gets
    def get_order_number(self):
        return self.__order_number

    def get_car(self):
        return self.__car

    def get_customer(self):
        return self.__customer

    def get_pickup_time(self):
        return self.__pickup_time

    def get_estimated_return_time(self):
        return self.__estimated_return_time

    def get_pickup_branch_name(self):
        return self.__pickup_branch_name

    def get_return_branch_name(self):
        return self.__return_branch_name

    def get_insurance_total(self):
        return self.__insurance_total

    def get_extra_insurance_total(self):
        return self.__extra_insurance_total

    def get_kilometer_allowance_per_day(self):
        return self.__kilometer_allowance_per_day

    def get_total_cost(self):
        return self.__total_cost

    def get_remaining_debt(self):
        return self.__remaining_debt

    def get_kilometers_driven(self):
        return self.__kilometers_driven

    def get_return_time(self):
        return self.__return_time

    def get_key(self):
        return self.__order_number

    def get_name(self):
        return "".join(
            self.get_customer().get_name(),
            ": ",
            self.get_car().get_name()
        )

    # Sets
    def set_order_number(self, order_number):
        self.__order_number = order_number

    def set_car(self, car):
        self.__car = car

    def set_customer(self, customer):
        self.__customer = customer

    def set_pickup_time(self, pickup_time):
        self.__pickup_time = pickup_time

    def set_estimated_return_time(self, estimated_return_time):
        self.__estimated_return_time = estimated_return_time

    def set_pickup_branch_name(self, pickup_branch_name):
        self.__pickup_branch_name = pickup_branch_name

    def set_return_branch_name(self, return_branch_name):
        self.__return_branch_name = return_branch_name

    def set_insurance_total(self, insurance_total):
        self.__insurance_total = insurance_total

    def set_extra_insurance_total(self, extra_insurance_total):
        self.__extra_insurance_total = extra_insurance_total

    def set_kilometer_allowance_per_day(self, kilometer_allowance_per_day):
        self.__kilometer_allowance_per_day = kilometer_allowance_per_day

    def set_total_cost(self, total_cost):
        self.__total_cost = total_cost

    def set_remaining_debt(self, remaining_debt):
        self.__remaining_debt = remaining_debt

    def set_kilometers_driven(self, kilometers_driven):
        self.__kilometers_driven = kilometers_driven

    def set_return_time(self, return_time):
        self.__return_time = return_time
