from models.model import Model
import typing


class Branch(Model):
    def __init__(self, name: str, address: str):
        self.__name = name
        self.__address = address

    def csv_repr(self):
        return self.get_dict()

    def get_dict(self):
        return {
            "name": self.__name,
            "address": self.__address
        }

    def __eq__(self, other):
        return self.__name == other.__name

    def get_name(self):
        return self.__name

    def get_key(self):
        return self.__name
