from repositories.admin_repository import AdminRepository
from repositories.salesperson_repository import SalespersonRepository
from models.salesperson import Salesperson


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
