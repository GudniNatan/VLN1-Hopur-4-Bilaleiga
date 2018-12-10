from repositories.repository import Repository
from models.customer import Customer
from datetime import date


class CustomerRepository(Repository):
    _FILENAME = "./data/Customers.csv"
    _TYPE = Customer
    _PRIMARY_KEY = "driver_licence_id"  # name of primary key
    _CSV_ROW_NAMES = [
        "driver_licence_id", "personal_id", "first_name", "last_name",
        "birthdate", "phone_number", "email", "cc_holder_first_name",
        "cc_holder_last_name", "ccn", "cc_exp_date"
    ]

    def dict_to_model_object(self, customer_dict):
        birthdate = date.fromisoformat(customer_dict["birthdate"])
        cc_expiry_date = date.fromisoformat(customer_dict["birthdate"])
        customer_dict["birthdate"] = birthdate
        return Customer(**customer_dict)
