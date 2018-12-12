from repositories.admin_repository import AdminRepository
from repositories.salesperson_repository import SalespersonRepository
from repositories.branch_repository import BranchRepository
from repositories.rent_order_repository import RentOrderRepository
from models.salesperson import Salesperson
from datetime import date, time, datetime
from math import inf
from models.branch import Branch
from models.car import Car
from models.customer import Customer
from models.rent_order import RentOrder

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
        raise ValueError("Rangt notendanafn eða lykilorð")

    def validate_salesperson(self, username, password,
                             name, email, phone):
        if not (username and password and name and email and phone):
            raise ValueError("Það er nauðsynlegt að fylla út öll gildin.")
        email = self.validate_email(email)
        phone = self.validate_phone_number(phone)
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
        date_formats = ["%Y-%m-%d", "%m/%y", "%d/%m/%Y", "%d-%m-%Y"]
        definitely_date = None
        for date_format in date_formats:
            try:
                definitely_date = datetime.strptime(maybe_date, date_format)
            except ValueError:
                continue
            break
        else:
            error_str = "{} þarf að vera dagsetning á forminu ÁÁÁÁ-MM-DD. "
            error_str += "{} er ekki gilt."
            raise ValueError(error_str.format(name, maybe_date))
        return definitely_date.date()

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

    def validate_datetime(self, datetime_str):
        try:
            a_datetime = datetime.fromisoformat(datetime_str)
        except ValueError:
            try:
                a_datetime = datetime.strptime(datetime_str, "%d/%m/%Y")
            except ValueError:
                raise ValueError(
                    "Dagsetning þarf að vera á forminu ÁÁÁÁ-MM-DD"
                )

    def validate_str(self, some_str, name):
        some_str = some_str.strip()
        if not some_str:
            raise ValueError(
                "Þarf að fylla út: {}.".format(name)
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

    def validate_phone_number(self, phone_number):
        phone_number = phone_number.strip()
        phone_number = phone_number.replace("-", "")
        phone_number = phone_number.replace(" ", "")
        if len(phone_number) != 7 and len(phone_number) != 10:
            raise ValueError("Ekki gilt símanúmer")
        return phone_number

    def validate_personal_id(self, personal_id_number):
        personal_id_number = personal_id_number.strip()
        personal_id_number = personal_id_number.replace("-", "")
        personal_id_number = personal_id_number.replace(" ", "")
        if not (9 <= len(personal_id_number) <= 10):
            raise ValueError("Ekki gild Kennitala/SSN")
        return personal_id_number

    def validate_email(self, email):
        if email.count('@') != 1:
            raise ValueError("Ekki gilt netfang")
        elif email.split("@")[1].count(".") != 1:
            raise ValueError("Ekki gilt netfang")
        return email

    def validate_ccn(self, ccn):
        ccn = ccn.strip().replace("-", "").replace(" ", "")
        # Uses modified https://en.wikipedia.org/wiki/Luhn_algorithm
        # to check credit card validity
        LUHN_ODD_LOOKUP = (0, 2, 4, 6, 8,
                           1, 3, 5, 7, 9)  # sum_of_digits (index * 2)
        try:
            evens = sum(int(p) for p in ccn[-1::-2])
            odds = sum(LUHN_ODD_LOOKUP[int(p)] for p in ccn[-2::-2])
            if (evens + odds) % 10 == 0:
                return ccn
        except ValueError:  # Raised if an int conversion fails
            pass
        raise ValueError("Ekki gilt kreditkortanúmer")

    def validate_car(
            self, license_plate_number: str, model: str,
            category: str, wheel_count: int, drivetrain: str,
            automatic_transmission: bool, seat_count: int,
            extra_properties: set, kilometer_count: int,
            current_branch=None,
            ):

        valid_license_plate = self.validate_str(license_plate_number)
        valid_model = self.validate_str(model)
        valid_category = self.validate_str(category)
        valid_wheel_count = self.validate_int(wheel_count)
        valid_drivetrain = self.validate_str(drivetrain)
        automatic_transmission_upper = self.validate_str(automatic_shift) == "J"
        valid_automatic_transmission = automatic_transmission_upper
        valid_seat_count = self.validate_int(seat_count)
        valid_extra_properties = self.validate_set
        valid_kilometer_count = self.validate_int

        if current_branch is None:
            branch_repo = BranchRepository()
            valid_current_branch = branch_repo.get_all()[0]
        else:
            if type(current_branch) == Branch:
                valid_current_branch = current_branch
            else:
                raise ValueError("Útibú er ekki gilt.")

        return Car(
            valid_license_plate, valid_model, valid_category,
            valid_wheel_count, valid_drive_train, automatic_shift_upper,
            valid_automatic_shift, valid_seat_count, valid_extra_properties,
            valid_kilometer_count
        )

    def validate_customer(
            self, driver_license_id: str, personal_id: str,
            first_name: str, last_name: str, birthdate: str, phone_number: str,
            email: str, cc_holder_first_name: str, cc_holder_last_name: str,
            ccn: str, cc_exp_date: str
            ):
        driver_license_id = self.validate_str(
            driver_license_id, "Ökuskírteinisnúmer"
        )
        personal_id = self.validate_str(personal_id, "Kennitala/SSN")
        first_name = self.validate_str(first_name, "Fornafn")
        last_name = self.validate_str(last_name, "Eftirnafn")
        birthdate = self.validate_date(birthdate, "Fæðingardagur")
        phone_number = self.validate_phone_number(phone_number)
        email = self.validate_email(email)
        cc_holder_first_name = self.validate_str(
            cc_holder_first_name, "Fornafn kreditkortahandhafa"
        )
        cc_holder_last_name = self.validate_str(
            cc_holder_last_name, "Eftirnafn kreditkortahandhafa"
        )
        ccn = self.validate_ccn(ccn)
        cc_exp_date = self.validate_date(
            cc_exp_date, "Fyrningardagsetning (MM/YY)"
        )
        return Customer(
            driver_license_id, personal_id, first_name, last_name, birthdate,
            phone_number, email, cc_holder_first_name, cc_holder_last_name,
            ccn, cc_exp_date
        )

    def validate_order(
            self, car, customer, pickup_date, pickup_time, est_return_date,
            est_return_time, pickup_branch_name, return_branch_name,
            include_extra_insurance, kilometer_allowance_per_day, total_cost,
            remaining_debt, kilometers_driven, return_time
            ):
        orders = RentOrderRepository().get_all()
        if orders:
            order_number = max(orders, key=RentOrder.get_key) + 1
        else:
            order_number = 1
        print(order_number)
        raise NotImplementedError()
