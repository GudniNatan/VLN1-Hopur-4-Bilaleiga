from repositories.admin_repository import AdminRepository
from repositories.salesperson_repository import SalespersonRepository


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