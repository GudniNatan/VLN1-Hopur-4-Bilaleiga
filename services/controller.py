from abc import ABC, abstractmethod
from ui.car_rental_ui import CarRentalUI
from repositories.salesperson_repository import SalespersonRepository
from repositories.admin_repository import AdminRepository


class Controller(ABC):
    def __init__(self, service, priority_controller=False):
        self._service = service
        self._menu_stack = list()
        self._ui = CarRentalUI()
        self._priority_controller = priority_controller

    @abstractmethod
    def main(self):
        pass

    def get_pop_limit(self):
        return self._priority_controller

    def get_user(self, username):
        admin_repo = AdminRepo()
        sales_repo = SalespersonRepo()
        administrators = admin_repo.get_all()
        salespeople = sales_repo.get_all()
        for staff in administrators + salespeople:
            if staff.get_user() == username:
                return staff

    def controller_back():
        self._service.pop()

    def controller_quit():
        self._service.pop_to_limit()

    def handle_return_selection(selection):
        if selection == "B":
            self.controller_back()
        elif selection == "Q":
            self.controller_quit()
