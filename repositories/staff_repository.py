from repositories.repository import Repository
from models.staff import Staff


class StaffRepository(Repository):
    _FILENAME = "./data/Staff.csv"
    _TYPE = Staff
    _PRIMARY_KEY = "username"  # name of primary key
    _CSV_ROW_NAMES = ["username", "password", "name",
                      "email", "phone"]

    def dict_to_model_object(self, staff_dict):
        return self._TYPE(**staff_dict)
