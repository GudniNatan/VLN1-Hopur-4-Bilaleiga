from repositories.admin_repository import AdminRepository
from repositories.salesperson_repository import SalespersonRepository
from repositories.branch_repository import BranchRepository
from repositories.rent_order_repository import RentOrderRepository
from repositories.car_repository import CarRepository
from repositories.customer_repository import CustomerRepository
from repositories.price_list_repository import PriceListRepository
from models.salesperson import Salesperson
from datetime import date, time, datetime, timedelta
from math import inf
from models.branch import Branch
from models.car import Car
from models.customer import Customer
from models.rent_order import RentOrder
from services.utils import Utils

# This is a class in which the methods take in some user inputted strings and
# the names of whatever the input field is. The methods will return objects of
# specified types. If there is some error in the input the class will raise a
# ValueError with a human-readable, Icelandic error message.


class Validation(object):
    def __init__(self):
        self.__admin_repo = AdminRepository()
        self.__salesperson_repo = SalespersonRepository()
        self.__utils = Utils()

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

    def validate_date(self, maybe_date, name=''):
        date_formats = ["%Y-%m-%d", "%d-%m-%Y"]
        seperators = [" ", "/", ":"]
        definitely_date = None
        maybe_date = maybe_date.strip()
        for seperator in seperators:
            maybe_date = maybe_date.replace(seperator, "-")
        for date_format in date_formats:
            try:
                definitely_date = datetime.strptime(maybe_date, date_format)
                return definitely_date.date()
            except ValueError:
                continue
        error_str = "{} þarf að vera dagsetning á forminu ÁÁÁÁ-MM-DD. "
        error_str += "'{}' er ekki gilt."
        raise ValueError(error_str.format(name, maybe_date))

    def validate_ccn_exp_date(self, maybe_date, name=""):
        error_str = "{} þarf að vera dagsetning á forminu MM-ÁÁ. "
        error_str += "'{}' er ekki gilt."
        date_format = "%m-%y"
        seperators = [" ", "/", ":"]
        definitely_date = None
        for seperator in seperators:
            maybe_date = maybe_date.replace(seperator, "-")
        try:
            definitely_date = datetime.strptime(maybe_date, date_format)
            if datetime.now() < definitely_date:
                return definitely_date.date()
            else:
                error_str = "{} er útrunnin. "
                error_str += "'{}' er ekki gilt."
                raise ValueError()
        except ValueError:
            raise ValueError(error_str.format(name, maybe_date))

    def validate_time(self, maybe_time, name=''):
        maybe_time = maybe_time.strip()
        if not name:
            name = "Tími"
        try:
            definitely_time = time.fromisoformat(maybe_time)
        except ValueError:
            error_str = "{}: '{}' er ekki gildur tími".format(name, maybe_time)
            raise ValueError(error_str)
        return definitely_time

    def validate_datetime_by_parts(self, date_str, time_str, name):
        a_date = self.validate_date(date_str, name + " dagsetning")
        a_time = self.validate_time(time_str, name + " tími")
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
            error_str = "{} þarf að vera rauntala. '{}' er ekki rauntala."
            error_str_format = error_str.format(name, some_float)
            raise ValueError(error_str_format)
        return valid_float

    def validate_phone_number(self, phone_number):
        phone_number = phone_number.strip()
        phone_number = phone_number.replace("-", "")
        phone_number = phone_number.replace(" ", "")
        if len(phone_number) < 7:
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
        elif email.split("@")[1].count(".") == 0:
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
            automatic_transmission: str, seat_count: int,
            extra_properties: set, kilometer_count: int,
            current_branch=None,
            ):

        valid_license_plate = self.validate_str(
            license_plate_number, "Bílnúmer"
        )
        valid_model = self.validate_str(model, "Model")
        valid_category = self.validate_category_in_repo(category)
        valid_wheel_count = self.validate_int(wheel_count, "Wheel count")
        valid_drivetrain = self.validate_str(drivetrain, "Drivetrain")
        valid_automatic_transmission = Utils.process_yes_no_answer(
            self, automatic_transmission
        )
        valid_seat_count = self.validate_int(seat_count, "Seat count")
        valid_extra_properties = self.validate_set(extra_properties)
        valid_kilometer_count = self.validate_int(
            kilometer_count, "Kilometer count"
        )
        valid_current_branch = self.validate_branch_in_repo(current_branch)

        return Car(
            valid_license_plate, valid_model, valid_category,
            valid_wheel_count, valid_drivetrain, valid_automatic_transmission,
            valid_seat_count, valid_extra_properties, valid_kilometer_count,
            valid_current_branch
        )

    def validate_customer(
            self, driver_license_id: str, personal_id: str, email: str,
            first_name: str, last_name: str, birthdate: str, phone_number: str,
            cc_holder_first_name: str, cc_holder_last_name: str,
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
        cc_exp_date = self.validate_ccn_exp_date(
            cc_exp_date, "Fyrningardagsetning"
        )
        return Customer(
            driver_license_id, personal_id, first_name, last_name, birthdate,
            phone_number, email, cc_holder_first_name, cc_holder_last_name,
            ccn, cc_exp_date
        )

    def validate_category_in_repo(self, category_name):
        try:
            category = PriceListRepository().get(category_name)
        except ValueError:
            categories = PriceListRepository().get_all()
            category_str_list = [
                category["category"] for category in categories
            ]
            category_str = ", ".join(category_str_list)
            error_msg = " ".join((
                "'", category_name, "' er ekki gildur flokkur.",
                "Þetta eru gildir flokkar:\n", *category_str_list, "\n"
            ))
            raise ValueError(error_msg)
        return category

    def validate_branch_in_repo(self, branch_name):
        try:
            branch = BranchRepository().get(branch_name)
        except ValueError:
            branches = BranchRepository().get_all()
            if branch_name is None:
                if branches:
                    return branches[0]
            branch_str_list = [branch.get_name() for branch in branches]
            branch_str = ", ".join(branch_str_list)
            error_msg = "".join((
                "'", str(branch_name), "' er ekki gilt útibú.",
                "Þetta eru gild útibú:\n", branch_str
            ))
            raise ValueError(error_msg)
        return branch

    def get_next_order_number(self):
        orders = RentOrderRepository().get_all()
        if orders:
            last_order = max(orders, key=RentOrder.get_key)
            order_number = last_order.get_order_number() + 1
        else:
            order_number = 1
        return order_number

    def validate_order(
            self, car, customer, pickup_date, pickup_time, est_return_date,
            est_return_time, pickup_branch_name, return_branch_name,
            include_extra_insurance,
            ):
        order_number = self.get_next_order_number()
        try:
            if type(car) != Car:
                car = CarRepository().get(car)
        except ValueError:
            error_msg = "".join((
                "Fann ekki þetta bílnúmer: '", car, "'",
                "\n Það er hægt að bæta við bílum í Bílaskránni."
            ))
            raise ValueError(error_msg)
        try:
            customer = CustomerRepository().get(customer)
        except ValueError:
            error_msg = "".join((
                "Viðskiptavinurinn fannst ekki ",
                "Nauðsynlegt er að viðskiptavinurnn sé skráður ",
                "áður en hann pantar bíl. "
            ))
            raise ValueError(error_msg)
        pickup_datetime = self.validate_datetime_by_parts(
            pickup_date, pickup_time, "Pickup"
        )
        est_return_datetime = self.validate_datetime_by_parts(
            est_return_date, est_return_time, "Estimated return time"
        )
        pickup_branch = self.validate_branch_in_repo(
            pickup_branch_name
        )
        return_branch = self.validate_branch_in_repo(
            return_branch_name
        )
        extra_insurance = self.__utils.process_yes_no_answer(
            include_extra_insurance
        )
        if extra_insurance is None:
            extra_insurance = False
        base_cost = self.__utils.calculate_base_cost(
            car, pickup_datetime, est_return_datetime
        )
        kilometers_driven = None
        return_time = None
        return RentOrder(
            order_number, car, customer, pickup_datetime, est_return_datetime,
            pickup_branch.get_name(), return_branch.get_name(),
            extra_insurance, base_cost
        )

    def assemble_order(self, car, customer, date_range,
                       pickup_branch, return_branch):
        return RentOrder(
            self.get_next_order_number(), car, customer, date_range[0],
            date_range[1], pickup_branch.get_name(), return_branch.get_name(),
        )

    def validate_rent_range(self, from_date, to_date):
        from_date = self.validate_datetime_by_parts(
                from_date[0], from_date[1], "Sótt"
        )
        to_date = self.validate_datetime_by_parts(
                to_date[0], to_date[1], "Skilað"
        )
        range_delta = to_date - from_date
        if range_delta < timedelta(days=1):
            raise ValueError("Leigutímabil verður að vera minnst 24 klst.")
        if from_date < datetime.now():
            raise ValueError("Leigutímabilið má ekki vera í fortíðinni")
        return (from_date, to_date)