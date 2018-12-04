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
        return {"username": self.__username, "password": self.__model,
                "name": self.__seat_count, "email": self.__automatic_shift,
                "phone": self.__phone}

    def get_dict(self):
        return self.csv_repr()

    def __eq__(self, other):
        return self.__username == other.__username
