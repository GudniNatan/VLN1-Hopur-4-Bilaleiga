from repositories.admin_repository import AdminRepository
from repositories.salesperson_repository import SalespersonRepository
from models.salesperson import Salesperson
from datetime import date, time, datetime
from math import inf
from models.branch import Branch
from repositories.branch_repository import BranchRepository
from models.car import Car

# This is a class in which the methods take in some user inputted strings and
# the names of whatever the input field is. The methods will return objects of
# specified types. If there is some error in the input the class will raise a
# ValueError with a human-readable, Icelandic error message.


class Validation(object):
    def __init__(self):
        self.__admin_repo = AdminRepository()
        self.__salesperson_repo = SalespersonRepository()

    def validate_login(self, username, password):
        admins = self.__admin_repo.get_all()
        salespeople = self.__salesperson_repo.get_all()
        staff = admins + salespeople
        for person in staff:
            if person.get_username() == username:
                if person.get_password() == password:
                    return person
        return None

    def validate_salesperson(self, username, password,
                             name, email, phone):
        if not (username and password and name and email and phone):
            raise ValueError("Það er nauðsynlegt að fylla út öll gildin.")
        if email.count('@') != 1:
            raise ValueError("Ekki gilt netfang")
        phone = phone.replace("-", "")
        phone = phone.replace(" ", "")
        if len(phone) != 7 and len(phone) != 10:
            raise ValueError("Ekki gilt símanúmer")
        name = name.capitalize()
        salesperson = Salesperson(username, password, name, email, phone)
        return salesperson

    def validate_int(self, maybe_int, name):
        try:
            definitely_int = int(maybe_int)
        except ValueError:
            raise ValueError("{} þarf að vera tala".format(name))
        return definitely_int

    def validate_date(self, maybe_date, name):
        try:
            definitely_date = date.fromisoformat(maybe_date)
        except ValueError:
            error_str = "{} þarf að vera dagsetning á forminu ÁÁÁÁ-MM-DD. "
            error_str += "{} er ekki gilt."
            raise ValueError(error_str.format(name, maybe_date))
        return definitely_date

    def validate_time(self, maybe_time):
        try:
            definitely_time = time.fromisoformat(maybe_time)
        except ValueError:
            error_str = "Tími: {} er ekki gildur tími".format(maybe_time)
            raise ValueError(error_str)
        return definitely_time

    def validate_datetime_by_parts(self, date_str, time_str, name):
        a_date = self.validate_date(date_str, name)
        a_time = self.validate_time(time_str, name)
        a_datetime = datetime.combine(a_date, a_time)
        return a_datetime

    def validate_datetime(self, datetime_str, name):

        pass

    def validate_str(self, some_str, name):
        some_str = some_str.strip()
        if not some_str:
            raise ValueError(
                "Reiturinn fyrir {} má ekki vera tómur.".format(name)
            )
        return some_str

    def validate_set(self, some_set, delimiter=", "):
        valid_set = set()
        set_list = some_set.split(delimiter)
        for a_string in set_list:
            valid_set.add(a_string)
        return valid_set

    def validate_float(self, some_float, name):
        try:
            valid_float = float(some_float)
        except ValueError:
            error_str = "{} þarf að vera rauntala. {} er ekki rauntala."
            error_str_format = error_str.format(name, some_float)
            raise ValueError(error_str_format)
        return valid_float

    def validate_car(
            self, license_plate, model, price_per_day,
            extra_insurance_per_day, category, wheel_count,
            drive_train, automatic_shift, seat_count, door_count,
            weight, fuel_type, fuel_efficiency, extra_properties,
            kilometer_count, horsepower, current_branch=None
            ):

        valid_license_plate = self.validate_str(license_plate)
        valid_model = self.validate_str(model)
        valid_price_per_day = self.validate_int(price_per_day)
        valid_extra_insurance_per_day = self.validate_str(
            extra_insurance_per_day
        )
        valid_category = self.validate_str(category)
        valid_wheel_count = self.validate_int(wheel_count)
        valid_drive_train = self.validate_str(drive_train)
        automatic_shift_upper = self.validate_str(automatic_shift) == "J"
        valid_automatic_shift = automatic_shift_upper
        valid_seat_count = self.validate_int(seat_count)
        valid_door_count = self.validate_int(door_count)
        valid_weight = self.validate_int(weight)
        valid_fuel_type = self.validate_str
        valid_fuel_efficiency = self.validate_float(fuel_efficiency) 
        valid_extra_properties = self.validate_set
        valid_kilometer_count = self.validate_int
        valid_horsepower = self.validate_int(horsepower)

        if current_branch is None:
            branch_repo = BranchRepository()
            valid_current_branch = branch_repo.get_all()[0]
        else:
            if type(current_branch) == Branch:
                valid_current_branch = current_branch
            else:
                raise ValueError("Útibú er ekki gilt.")

        return Car(
            valid_license_plate, valid_model, valid_price_per_day,
            valid_extra_insurance_per_day, valid_category, valid_wheel_count,
            valid_drive_train, valid_automatic_shift, valid_seat_count,
            valid_door_count, valid_weight, valid_fuel_type,
            valid_fuel_efficiency, valid_extra_properties,
            valid_kilometer_count, valid_horsepower
        )
