from models.model import Model


class Staff(Model):
    def __init__(self, username: str, password: str,
                 name: str, email: str, phone: str):
        self._username = username
        self._password = password
        self._name = name
        self._email = email
        self._phone = phone

    def csv_repr(self):
        return {"username": self._username, "password": self._password,
                "name": self._name, "email": self._email,
                "phone": self._phone}

    def get_dict(self):
        return self.csv_repr()

    def __eq__(self, other):
        return self._username == other._username

    # Get
    def get_username(self):
        return self._username

    def get_password(self):
        return self._password

    def get_name(self):
        return self._name

    # Set
    def set_username(self, username):
        self._username = username

    def set_password(self, password):
        self._password = password

    def set_name(self, name):
        self._name = name
