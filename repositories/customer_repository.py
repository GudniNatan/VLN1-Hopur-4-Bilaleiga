from repositories.repository import Repository
from models.customer import Customer
from datetime import date


class CustomerRepository(Repository):
    _FILENAME = "./data/Customers.csv"
    _TYPE = Customer
    _PRIMARY_KEY = "driver_license_id"  # name of primary key
    _CSV_ROW_NAMES = [
        "driver_license_id", "personal_id", "email", "first_name", "last_name",
        "birthdate", "phone_number", "cc_holder_first_name",
        "cc_holder_last_name", "ccn", "cc_exp_date"
    ]

    def dict_to_model_object(self, customer_dict):
        birthdate = date.fromisoformat(customer_dict["birthdate"])
        cc_exp_date = date.fromisoformat(customer_dict["cc_exp_date"])
        customer_dict["birthdate"] = birthdate
        customer_dict["cc_exp_date"] = cc_exp_date
        return Customer(**customer_dict)
