from abc import ABC, abstractmethod
from ui.car_rental_ui import CarRentalUI
from repositories.salesperson_repository import SalespersonRepository
from repositories.admin_repository import AdminRepository
from services.validation import Validation


class Controller(ABC):
    def __init__(self, service, priority_controller=False):
        self._service = service
        self._menu_stack = list()
        self._ui = CarRentalUI()
        self._priority_controller = priority_controller
        self._active = False
        self._validation = Validation()

    def main(self):
        self._active = True
        menu_stack = self._menu_stack
        while menu_stack and self._active:
            fun, menu = menu_stack[-1]
            selection, values = menu.get_input()
            self.handle_return_selection(selection)
            if selection is not None:
                fun(menu, selection, values)
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

    def menu_back(self):
        self._menu_stack.pop()

    def controller_quit(self):
        self._active = False
        self._service.pop_to_limit()

    def controller_back(self):
        self._active = False
        self._service.pop()

    def controller_restart(self):
        self.controller_back()
        controller = type(self)(self._service)
        self._service.add(controller)

    def handle_return_selection(self, selection):
        if selection == "B":
            self.menu_back()
        elif selection == "Q":
            self.controller_quit()
        else:
            return selection

    def pop(self):
        self._menu_stack.pop()

    def append(self, menu_function):
        self._menu_stack.append(menu_function)
