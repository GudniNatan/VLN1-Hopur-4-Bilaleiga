from models.Model import Model
import typing


class Car(Model):
    def __init__(self, licence_plate_number: str, model: str, seat_count: int,
                 automatic_shift: bool, category: str):
        self.licence_plate_number = licence_plate_number
        self.model = model
        self.seat_count = seat_count
        self.automatic_shift = automatic_shift
        self.category = category

    def csv_repr(self):
        return {"licence_plate_number": self.licence_plate_number,
                "model": self.model, "seat_count": self.seat_count,
                "automatic_shift": self.automatic_shift}

    def get_dict(self):
        return self.csv_repr()

    def __eq__(self, other):
        return self.licence_plate_number == other.licence_plate_number
