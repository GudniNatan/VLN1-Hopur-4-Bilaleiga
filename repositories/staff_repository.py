from repositories.repository import Repository
from models.staff import Staff


class StaffRepository(Repository):
    _FILENAME = "./data/Staff.csv"
    _TYPE = Staff
    _PRIMARY_KEY = "Notandanafn"  # name of primary key
    _CSV_ROW_NAMES = ["Notandanafn", "Lykilorð", "Nafn",
                      "Netfang", "Símanúmer"]

    def dict_to_model_object(self, staff_dict):
        args_list = [value for value in staff_dict.values()]
        return self._TYPE(*args_list)
