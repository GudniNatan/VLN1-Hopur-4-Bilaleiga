from services.controller import Controller
from repositories.rent_order_repository import RentOrderRepository
from ui.menu import Menu
from models.admin import Admin


class ManageOrdersController(Controller):
    def __init__(self, service, shortcut_to_register=False,
                 priority_controller=False):
        super().__init__(service, priority_controller)
        self.__controller_header = "Pantanaskrá"
        self.__order_repo = RentOrderRepository()
        self.__selected_order = None
        self._menu_stack.append(self.__make_main_menu())

    def go_to_search(self, values, menu):
        pass

    def go_to_search_all(self, values, menu):
        pass

    def go_to_create(self, values, menu):
        pass

    def __make_main_menu(self):
        header = self.__controller_header
        header += "\n\nLeita að pöntun"
        inputs = [{"prompt": "Pöntunarnúmer:"},
                  {"prompt": "Kennitala viðskiptarvinar:"},
                  {"prompt": "Bílnúmer:"},
                  {"prompt": "Fela óvirkar pantanir (J/N):"}]
        search = self.go_to_search
        search_all = self.go_to_search_all
        create = self.go_to_create
        options = [
            {"description": "Leita", "value": search},
            {"description": "Sjá allar pantanir", "value": search_all},
            {"description": "Bæta við pöntun", "value": create}
        ]
        footer = "Sláðu inn þær upplýsingar sem þú vilt leita eftir. "
        footer += "Ekki er nauðsynlegt að fylla út alla reitina."
        menu = Menu(
            header=header, inputs=inputs, options=options, footer=footer,
            can_submit=False, back_function=self.back, stop_function=self.stop,
            max_options_per_page=10
        )
        return menu
