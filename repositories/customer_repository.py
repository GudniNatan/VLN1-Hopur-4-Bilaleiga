from repositories.repository import Repository
from models.customer import Customer
from datetime import date, datetime


class CustomerRepository(Repository):
    _FILENAME = "./data/Customers.csv"
    _TYPE = Customer
    _PRIMARY_KEY = "Ökuskírteinisnúmer"  # name of primary key
    _CSV_ROW_NAMES = [
        "Ökuskírteinisnúmer", "Kennitala", "Netfang", "Fornafn", "Eftirnafn",
        "Fæðingar dagssetning", "Símanúmer", "Fornafn kortahafa",
        "Eftirnafn kortahafa", "Kortanúmer", "Gildistími korts"
    ]

    def dict_to_model_object(self, customer_dict):
        exp_str = customer_dict["Gildistími korts"]
        try:
            cc_exp_date = datetime.strptime(exp_str, "%m/%y").date()
        except ValueError:
            cc_exp_date = date.fromisoformat(customer_dict["Gildistími korts"])
        birthdate = date.fromisoformat(customer_dict["Fæðingar dagssetning"])
        customer_dict["Fæðingar dagssetning"] = birthdate
        customer_dict["Gildistími korts"] = cc_exp_date
        args_list = [value for value in customer_dict.values()]
        return Customer(*args_list)
