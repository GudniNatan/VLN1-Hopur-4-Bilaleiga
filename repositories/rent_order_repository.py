from datetime import datetime
from repositories.repository import Repository
from repositories.car_repository import CarRepository
from repositories.customer_repository import CustomerRepository
from models.rent_order import RentOrder


class RentOrderRepository(Repository):
    _FILENAME = "./data/RentOrders.csv"
    _TYPE = RentOrder
    _PRIMARY_KEY = "Bókunar númer"  # name of primary key
    _CSV_ROW_NAMES = [
        "Bókunar númer", "Bíll", "Viðskiptavinur", "Sóttur þann",
        "Áætlaður skilatími", "Sóttur hjá", "Skilaður hjá",
        "Auka trygging", "Grunnkostnaður", "Eftirstaða borgunar",
        "Keyrðir kílómetrar", "Raunverulegur skilatími"
    ]

    def dict_to_model_object(self, rent_order_dict):
        order_number = int(rent_order_dict["Bókunar númer"])
        car = CarRepository().get(rent_order_dict["Bíll"])
        customer = CustomerRepository().get(rent_order_dict["Viðskiptavinur"])
        pickup_time = datetime.fromisoformat(rent_order_dict["Sóttur þann"])
        est_return_str = rent_order_dict["Áætlaður skilatími"]
        estimated_return_time = datetime.fromisoformat(est_return_str)
        pickup_branch_name = rent_order_dict["Sóttur hjá"]
        return_branch_name = rent_order_dict["Skilaður hjá"]
        base_cost = int(rent_order_dict["Grunnkostnaður"])
        extra_insurance = bool(rent_order_dict["Auka trygging"])
        remaining_debt = int(rent_order_dict["Eftirstaða borgunar"])
        kilometers_driven = int(rent_order_dict["Keyrðir kílómetrar"])
        if rent_order_dict["Raunverulegur skilatími"]:
            return_time = datetime.fromisoformat(
                rent_order_dict["Raunverulegur skilatími"]
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
