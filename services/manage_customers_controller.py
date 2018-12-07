from services.controller import Controller
from repositories.customer_repository import CustomerRepository
from ui.menu import Menu


class ManageCustomersController(Controller):
    def __init__(self, service, shortcut_to_register=False,
                 priority_controller=False):
        super().__init__(service, priority_controller)
        if shortcut_to_register:
            pass
        else:
            self._menu_stack.append(self.__make_main_menu())
        self.__selected_customer = None

    # Operations
    # THIS IS NOT IMPLEMENDTED YET
    def go_to_search(self, values, menu):
        results = self.__search_salespeople(*values)
        search_menu = self.__make_search_result_menu(results)
        self._menu_stack.append(search_menu)

    def go_to_search_all(self, values, menu):
        for i in range(len(values)):
            values[i] = ""
        self.go_to_search(values, menu)

    def go_to_create(self, values, menu):
        new_salesperson_menu = self.__make_new_salesperson_menu()
        self._menu_stack.append(new_salesperson_menu)
