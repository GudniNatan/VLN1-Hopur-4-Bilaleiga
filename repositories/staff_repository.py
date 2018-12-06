from repositories.repository import Repository
from models.staff import Staff


class StaffRepository(Repository):
    _FILENAME = "./data/Staff.csv"
    _TYPE = Staff
    _PRIMARY_KEY = "username"  # name of primary key
    _CSV_ROW_NAMES = ["username", "password", "name",
                      "email", "phone"]

    def dict_to_model_object(self, car_dict):
        username = car_dict['username']
        password = car_dict['password']
        name = car_dict['name']
        email = car_dict['email']
        phone = car_dict['phone']
        return self._TYPE(username, password, name, email, phone)
