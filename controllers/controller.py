from abc import ABC, abstractmethod
from ui.car_rental_ui import CarRentalUI
from repositories.salesperson_repository import SalespersonRepository
from repositories.admin_repository import AdminRepository
from services.validation import Validation
from services.search import Search
from services.utils import Utils


class Controller(ABC):
    def __init__(self, service, priority_controller=False):
        self._service = service
        self._menu_stack = list()
        self._ui = CarRentalUI(self.back, self.stop)
        self._priority_controller = priority_controller
        self._active = False
        self._validation = Validation()
        self._search = Search()
        self._utils = Utils()

    def main(self):
        self._active = True
        menu_stack = self._menu_stack
        while menu_stack and self._active:
            menu = menu_stack[-1]
            a_function, values = menu.get_input()
            a_function(values, menu)
        if not menu_stack:
            self._service.pop()

    def get_pop_limit(self):
        return self._priority_controller

    def get_user(self, username):
        admin_repo = AdminRepository()
        sales_repo = SalespersonRepository()
        administrators = admin_repo.get_all()
        salespeople = sales_repo.get_all()
        for staff in administrators + salespeople:
            if staff.get_user() == username:
                return staff

    def back(self, values=None, menu=None):
        self._menu_stack.pop()

    def stop(self, values=None, menu=None):
        self.deactivate()
        self._service.pop_to_limit()

    def controller_back(self, values=None, menu=None):
        self.deactivate()
        self._service.pop()

    def restart(self, values=None, menu=None):
        self.controller_back()
        controller = type(self)(self._service)
        self._service.add(controller)

    def pop(self, values=None, menu=None):
        self._menu_stack.pop()

    def append(self, menu_function):
        self._menu_stack.append(menu_function)

    def deactivate(self):
        self._active = False

    def go_to_search_all(self, values, menu):
        for i in range(len(values)):
            values[i] = ""
        self.go_to_search(values, menu)
