from models.model import Model


class Branch(Model):
    def __init__(self, name: str, address: str):
        self.__name = name
        self.__address = address

    def csv_repr(self):
        return self.get_dict()

    def get_dict(self):
        return {
            "Nafn": self.__name,
            "Heimilsfang": self.__address
        }

    def __eq__(self, other):
        return self.__name == other.__name

    def get_name(self):
        return self.__name

    def get_key(self):
        return self.__name

    def __str__(self):
        return self.__name
