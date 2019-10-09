from collections import OrderedDict
from models.model import Model
from datetime import date


class Customer(Model):
    def __init__(
            self, driver_license_id: str, personal_id: str, email: str,
            first_name: str, last_name: str, birthdate: date,
            phone_number: str, cc_holder_first_name: str,
            cc_holder_last_name: str, ccn: str, cc_exp_date: date,
    ):
        self.__driver_license_id = driver_license_id
        self.__personal_id = personal_id
        self.__email = email
        self.__first_name = first_name
        self.__last_name = last_name
        self.__birthdate = birthdate
        self.__phone_number = phone_number
        self.__cc_holder_first_name = cc_holder_first_name
        self.__cc_holder_last_name = cc_holder_last_name
        self.__ccn = ccn
        self.__cc_exp_date = cc_exp_date

    def csv_repr(self):
        customer_dict = self.get_dict()
        exp_date_str = self.__cc_exp_date.strftime("%m/%y")
        customer_dict['Fæðingar dagssetning'] = self.__birthdate.isoformat()
        customer_dict['Gildistími korts'] = exp_date_str
        return customer_dict

    def get_dict(self):
        return OrderedDict([
            ("Ökuskírteinisnúmer", self.__driver_license_id),
            ("Kennitala", self.__personal_id), ("Netfang", self.__email),
            ("Fornafn", self.__first_name), ("Eftirnafn", self.__last_name),
            ("Fæðingar dagssetning", self.__birthdate),
            ("Símanúmer", self.__phone_number),
            ("Fornafn kortahafa", self.__cc_holder_first_name),
            ("Eftirnafn kortahafa", self.__cc_holder_last_name),
            ("Kortanúmer", self.__ccn),
            ("Gildistími korts", self.__cc_exp_date)
        ])

    def __eq__(self, other):
        if isinstance(other, Customer):
            return self.__driver_license_id == other.__driver_license_id
        else:
            return self._username == str(other)

    def __str__(self):
        return "Nafn: {} {}\n\tÖkuskírteini: {}".format(
            self.__first_name, self.__last_name, self.__driver_license_id
        )

    # Get
    def get_driver_license_id(self):
        return self.__driver_license_id

    def get_personal_id(self):
        return self.__personal_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_birthdate(self):
        return self.__birthdate

    def get_phone_number(self):
        return self.__phone_number

    def get_cc_holder_first_name(self):
        return self.__cc_holder_first_name

    def get_cc_holder_last_name(self):
        return self.__cc_holder_last_name

    def get_ccn(self):
        return self.__ccn

    def get_cc_exp_date(self):
        return self.__cc_exp_date

    def get_email(self):
        return self.__email

    def get_name(self):
        return "{} {}".format(self.__first_name, self.__last_name)

    def get_key(self):
        return self.__driver_license_id

    # Set
    def set_driver_license_id(self, driver_license_id):
        self.__driver_license_id = driver_license_id

    def set_personal_id(self, personal_id):
        self.__personal_id = personal_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_birthdate(self, birthdate):
        self.__birthdate = birthdate

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_cc_holder_first_name(self, cc_holder_first_name):
        self.__cc_holder_first_name = cc_holder_first_name

    def set_cc_holder_last_name(self, cc_holder_last_name):
        self.__cc_holder_last_name = cc_holder_last_name

    def set_ccn(self, ccn):
        self.__ccn = ccn

    def set_cc_exp_date(self, cc_exp_date):
        self.__cc_exp_date = cc_exp_date

    def set_email(self, email):
        self.__email = email
