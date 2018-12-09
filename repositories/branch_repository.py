from repositories.repository import Repository
from models.branch import Branch
import typing


class BranchRepository(Repository):
    _FILENAME = "./data/Branches.csv"
    _TYPE = Branch
    _PRIMARY_KEY = "licence_plate_number"  # name of primary key
    _CSV_ROW_NAMES = ["licence_plate_number", "model", "seat_count",
                      "automatic_shift"]

    def dict_to_model_object(self, car_dict):
        licence_plate_number = car_dict['licence_plate_number']
        model = car_dict['model']
        seat_count = int(car_dict['seat_count'])
        automatic_shift = bool(car_dict['automatic_shift'])
        return Car(licence_plate_number, model, seat_count,
                   automatic_shift)
