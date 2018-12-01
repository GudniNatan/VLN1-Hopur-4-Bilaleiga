from models.Model import Model
import typing


class Car(Model):
    def __init__(self, branch_name: str, address: str, cars: list()):
        self.branch_name = branch_name
        self.address = address
        self.cars = cars

    def csv_repr(self):
        licence_plate_numbers = list()
        for car in self.cars:
            licence_plate_numbers.append(car.licence_plate_number)
        return {"branch_name": self.branch_name, "address": self.address,
                "cars": licence_plate_numbers}

    def get_dict(self):
        return {"branch_name": self.branch_name, "address": self.address,
                "cars": self.cars}
