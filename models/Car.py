from models.model import Model
import typing


class Car(Model):
    def __init__(self, licence_plate_number: str, model: str, seat_count: int,
                 automatic_shift: bool, category: str):
        self.__licence_plate_number = licence_plate_number
        self.__model = model
        self.__seat_count = seat_count
        self.__automatic_shift = automatic_shift
        self.__category = category

    def csv_repr(self):
        return {"licence_plate_number": self.__licence_plate_number,
                "model": self.__model, "seat_count": self.__seat_count,
                "automatic_shift": self.__automatic_shift}

    def get_dict(self):
        return self.csv_repr()

    def __eq__(self, other):
        return self.licence_plate_number == other.licence_plate_number

    # Get
    def get_licence_plate_number(self):
        return self.__licence_plate_number

    def get_model(self):
        return self.__model

    def get_seat_count(self):
        return self.__seat_count

    def get_automatic_shift(self):
        return self.__automatic_shift

    def get_category(self):
        return self.__category

    # Set
    def set_licence_plate_number(self, licence_plate_number):
        self.__licence_plate_number = licence_plate_number

    def set_model(self, model):
        self.__model = model

    def set_seat_count(self, seat_count):
        self.__seat_count = seat_count

    def set_automatic_shift(self, automatic_shift):
        self.__automatic_shift = automatic_shift

    def set_category(self, category):
        self.__category = category
