from repositories.repository import Repository
from repositories.branch_repository import BranchRepository
from models.car import Car


class CarRepository(Repository):
    _FILENAME = "./data/Cars.csv"
    _TYPE = Car
    _PRIMARY_KEY = "license_plate_number"  # name of primary key
    _CSV_ROW_NAMES = [
        "license_plate_number", "model", "category", "wheel_count",
        "drivetrain", "automatic_transmission", "seat_count",
        "extra_properties", "kilometer_count", "current_branch"
    ]

    def dict_to_model_object(self, car_dict):
        license_plate_number = car_dict['license_plate_number']
        model = car_dict['model']
        category = car_dict["category"]
        wheel_count = int(car_dict["wheel_count"])
        drivetrain = car_dict["drivetrain"]
        automatic_transmission = bool(car_dict['automatic_transmission'])
        seat_count = int(car_dict['seat_count'])
        extra_properties = set(car_dict['extra_properties'].split(","))
        kilometer_count = int(car_dict['kilometer_count'])
        current_branch = BranchRepository().get(car_dict['current_branch'])
        return Car(
            license_plate_number, model, category, wheel_count, drivetrain,
            automatic_transmission, seat_count, extra_properties,
            kilometer_count, current_branch
        )
