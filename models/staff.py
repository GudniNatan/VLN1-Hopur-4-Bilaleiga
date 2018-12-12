from models.model import Model


class Staff(Model):
    def __init__(self, username: str, password: str,
                 name: str, email: str, phone: str):
        self.__username = username
        self.__password = password
        self.__name = name
        self.__email = email
        self.__phone = phone

    def csv_repr(self):
        return {"username": self.__username, "password": self.__password,
                "name": self.__name, "email": self.__email,
                "phone": self.__phone}

    def get_dict(self):
        return self.csv_repr()

    def __eq__(self, other):
        if isinstance(other, Staff):
            return self.__username == other.__username
        else:
            return self.__username == str(other)

    def __str__(self):
        return "Nafn: {}\n\tNotendanafn: {}".format(self.__name,
                                                    self.__username)
    # Get
    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_name(self):
        return self.__name

    def get_email(self):
        return self.__email

    def get_phone(self):
        return self.__phone

    def get_key(self):
        return self.__username

    # Set
    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password

    def set_name(self, name):
        self.__name = name

    def set_email(self, email):
        self.__email = email

    def set_phone(self, phone):
        self.__phone = phone
