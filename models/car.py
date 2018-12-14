from models.model import Model
from models.branch import Branch
from collections import OrderedDict


class Car(Model):
    def __init__(
            self, license_plate_number: str, model: str,
            category: dict, wheel_count: int, drivetrain: str,
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
        car_dict["Núverandi útibú"] = car_dict["Núverandi útibú"].get_name()
        properties = car_dict["Aðrir eiginleikar"]
        property_string = ", ".join(properties)
        car_dict["Aðrir eiginleikar"] = property_string
        return car_dict

    def get_dict(self):
        return OrderedDict([
            ("Bílnúmer", self.__license_plate_number),
            ("Gerð", self.__model),
            ("Flokkur", self.__category["category"]),
            ("Fjöldi hjóla", self.__wheel_count),
            ("Drif", self.__drivetrain),
            ("Sjálfskiptur", self.__automatic_transmission),
            ("Fjöldi sæta", self.__seat_count),
            ("Aðrir eiginleikar", self.__extra_properties),
            ("Kílómetrafjöldi", self.__kilometer_count),
            ("Núverandi útibú", self.__current_branch),
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
        info_string = "{}\n\tFlokkur bíls: {}\n\t"
        info_string += "Sjalfskiptur: {}\n\tAukahlutir: {}"
        return info_string.format(
            self.__model, self.__category["category"],
            automatic_shift, ", ".join(self.__extra_properties)
        )

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

    def get_extra_properties(self):
        return self.__extra_properties
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

    def set_current_branch(self, current_branch):
        self.__current_branch = current_branch
