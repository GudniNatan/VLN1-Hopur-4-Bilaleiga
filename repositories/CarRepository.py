from repositories.Repository import Repository
from models.Car import Car
import csv
import typing


class CarRepository(Repository):
    _FILENAME = "./data/Cars.csv"
    _TYPE = Car
    _PRIMARY_KEY = "licence_plate_number"  # name of primary key
    _CSV_ROWS = ["licence_plate_number", "model", "seat_count",
                 "automatic_shift"]

    def dict_to_model_object(self, car_dict):
        licence_plate_number = car_dict['licence_plate_number']
        model = car_dict['model']
        seat_count = int(car_dict['seat_count'])
        automatic_shift = bool(car_dict['automatic_shift'])
        return Car(licence_plate_number, model, seat_count,
                   automatic_shift)
