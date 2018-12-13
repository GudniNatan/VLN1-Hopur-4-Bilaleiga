from models.model import Model
from models.branch import Branch
from collections import OrderedDict


class Car(Model):
    def __init__(
            self, license_plate_number: str, model: str,
            category: str, wheel_count: int, drivetrain: str,
            automatic_transmission: bool, seat_count: int,
            extra_properties: set, kilometer_count: int,
            current_branch: Branch,
            ):
        self.__license_plate_number = license_plate_number
        self.__model = model
        self.__category = category
        self.__wheel_count = wheel_count
        self.__drivetrain = drivetrain
        self.__automatic_transmission = automatic_transmission
        self.__seat_count = seat_count
        self.__extra_properties = extra_properties
        self.__kilometer_count = kilometer_count
        self.__current_branch = current_branch

    def csv_repr(self):
        car_dict = self.get_dict()
        car_dict["current_branch"] = car_dict["current_branch"].get_name()
        properties = car_dict["extra_properties"]
        property_string = ", ".join(properties)
        car_dict["extra_properties"] = property_string
        return car_dict

    def get_dict(self):
        return OrderedDict([
            ("license_plate_number", self.__license_plate_number),
            ("model", self.__model),
            ("category", self.__category["category"]),
            ("wheel_count", self.__wheel_count),
            ("drivetrain", self.__drivetrain),
            ("automatic_transmission", self.__automatic_transmission),
            ("seat_count", self.__seat_count),
            ("extra_properties", self.__extra_properties),
            ("kilometer_count", self.__kilometer_count),
            ("current_branch", self.__current_branch),
        ])

    def __eq__(self, other):
        if isinstance(other, Car):
            return self.__license_plate_number == other.__license_plate_number
        else:
            return self.__license_plate_number == str(other)

    def __str__(self):
        if self.__automatic_transmission:
            automatic_shift = "Já"
        else:
            automatic_shift = "Nei"
        info_string = "Flokkur bíls: {}\n\tGerð: {}\n\t"
        info_string += "Sjalfskiptur: {}\n\tKílómetrafjöldi: {}"
        return info_string.format(self.__category["category"], self.__model,
                                  automatic_shift, self.__kilometer_count)

    # Get
    def get_license_plate_number(self):
        return self.__license_plate_number

    def get_model(self):
        return self.__model

    def get_seat_count(self):
        return self.__seat_count

    def get_automatic_transmission(self):
        return self.__automatic_transmission

    def get_category(self):
        return self.__category

    def get_current_branch(self):
        return self.__current_branch

    def get_key(self):
        return self.__license_plate_number

    def get_name(self):
        return self.get_model()

    # Set
    def set_license_plate_number(self, license_plate_number):
        self.__license_plate_number = license_plate_number

    def set_model(self, model):
        self.__model = model

    def set_seat_count(self, seat_count):
        self.__seat_count = seat_count

    def set_automatic_shift(self, automatic_shift):
        self.__automatic_shift = automatic_shift

    def set_category(self, category):
        self.__category = category
