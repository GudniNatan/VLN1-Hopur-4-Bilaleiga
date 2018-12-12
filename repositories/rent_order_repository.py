from datetime import datetime
from repositories.repository import Repository
from repositories.car_repository import CarRepository
from repositories.customer_repository import CustomerRepository
from models.rent_order import RentOrder


class RentOrderRepository(Repository):
    _FILENAME = "./data/RentOrders.csv"
    _TYPE = RentOrder
    _PRIMARY_KEY = "order_number"  # name of primary key
    _CSV_ROW_NAMES = [
        "order_number", "car", "customer", "pickup_time",
        "estimated_return_time", "pickup_branch_name", "return_branch_name",
        "include_extra_insurance", "kilometer_allowance_per_day", "base_cost",
        "remaining_debt", "kilometers_driven", "return_time"
    ]

    def dict_to_model_object(self, rent_order_dict):
        order_number = int(rent_order_dict["order_number"])
        car = CarRepository().get(rent_order_dict["car"])
        customer = CustomerRepository().get(rent_order_dict["customer"])
        pickup_time = datetime.fromisoformat(rent_order_dict["pickup_time"])
        est_return_str = rent_order_dict["estimated_return_time"]
        estimated_return_time = datetime.fromisoformat(est_return_str)
        pickup_branch_name = rent_order_dict["pickup_branch_name"]
        return_branch_name = rent_order_dict["return_branch_name"]
        km_allowance_str = rent_order_dict["kilometer_allowance_per_day"]
        kilometer_allowance_per_day = int(km_allowance_str)
        base_cost = int(rent_order_dict["base_cost"])
        extra_insurance = bool(rent_order_dict["include_extra_insurance"])
        remaining_debt = int(rent_order_dict["remaining_debt"])
        kilometers_driven = int(rent_order_dict["kilometers_driven"])
        if rent_order_dict["return_time"]:
            return_time = datetime.fromisoformat(
                rent_order_dict["return_time"]
            )
        else:
            return_time = None
        return RentOrder(
            order_number, car, customer,
            pickup_time, estimated_return_time,
            pickup_branch_name, return_branch_name,
            extra_insurance, base_cost, remaining_debt,
            kilometers_driven, return_time
        )
