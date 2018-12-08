from repositories.admin_repository import AdminRepository
from repositories.salesperson_repository import SalespersonRepository
from models.salesperson import Salesperson
from datetime import date
from math import inf


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
            raise ValueError("{} þarf að vera dagsetning. {} er ekki gild dagsetning.".format(name, maybe_date))
        return definitely_date

    def validate_str(self, some_str, name):
        if not some_str.strip():
            raise ValueError("Reiturinn fyrir {} má ekki vera tómur.".format(name))
        return some_str.strip()
    
    def validate_set(self, some_set):
        valid_set = set()
        set_list = some_set.split(", ")
        for i in set_list:
            valid_str = validate_str(i)     #af hverju get ég ekki kallað í validate_str??
            valid_set.add(valid_str)
        return valid_set
        

    #def validate_car(self, license_plate:str, model:str, price_per_day:int, extra_insurance_per_day:int, category:str, 
    #               wheel_count=4, drive_train:str, automatic_shift:bool, seat_count:int, door_count:int, weight:int, 
    #               fuel_type:str, fuel_efficiency:float, emission:float, extra_properties:set, kilometer_count:int, 
    #               horsepower:int, current_branch:Branch)

    
