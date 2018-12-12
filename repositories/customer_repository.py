from repositories.repository import Repository
from models.customer import Customer
from datetime import date


class CustomerRepository(Repository):
    _FILENAME = "./data/Customers.csv"
    _TYPE = Customer
    _PRIMARY_KEY = "Ökuskírteinis númer"  # name of primary key
    _CSV_ROW_NAMES = [
        "Ökuskírteinis númer", "Kennitala", "Fornafn", "Eftirnafn",
        "Fæðingar dagssetning", "Símanúmer", "Netfang", "Fornafn kortahafa",
        "Eftirnafn kortahafa", "Kortanúmer", "Gildistími korts"
    ]

    def dict_to_model_object(self, customer_dict):
        birthdate = date.fromisoformat(customer_dict["Fæðingar dagssetning"])
        cc_exp_date = date.fromisoformat(customer_dict["Gildistími korts"])
        customer_dict["Fæðingar dagssetning"] = birthdate
        customer_dict["Gildistími korts"] = cc_exp_date
        return Customer(**customer_dict)
