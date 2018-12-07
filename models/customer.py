from models.model import Model
from datetime import date


class Customer(Model):
    def __init__(
            self, driver_licence_id: str, personal_id: str, first_name: str,
            last_name: str, birthdate: date, phone_number: str,
            cc_holder_first_name: str, cc_holder_last_name: str, ccn: str,
            cc_exp_date: str, email: str
            ):
        self.__driver_licence_id = driver_licence_id
        self.__personal_id = personal_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__birthdate = birthdate
        self.__phone_number = phone_number
        self.__cc_holder_first_name = cc_holder_first_name
        self.__cc_holder_last_name = cc_holder_last_name
        self.__ccn = ccn
        self.__cc_exp_date = cc_exp_date
        self.__email = email

    def csv_repr(self):
        return {"username": self._username, "password": self._password,
                "name": self._name, "email": self._email,
                "phone": self._phone}

    def get_dict(self):
        return self.csv_repr()

    def __eq__(self, other):
        if isinstance(other, Staff):
            return self._username == other._username
        else:
            return self._username == str(other)

    # Get
    def get_driver_licence_id(self):
        return self.__driver_licence_id

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

    # Set
    def set_driver_licence_id(self, driver_licence_id):
        self.__driver_licence_id = driver_licence_id

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
