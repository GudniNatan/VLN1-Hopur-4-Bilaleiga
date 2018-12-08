from services.controller import Controller
from repositories.car_repository import CarRepository
from ui.menu import Menu


class ManageCustomersController(Controller):
    def __init__(self, service, shortcut_to_register=False,
                 priority_controller=False):
        super().__init__(service, priority_controller)
        self.__controller_header = "Bílaskrá"
        self.__car_repo = CarRepository()
        self._menu_stack.append(self.__make_main_menu())