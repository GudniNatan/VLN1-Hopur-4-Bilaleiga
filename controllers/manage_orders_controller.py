from controllers.controller import Controller
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

    # Operations
    def go_to_search(self, values, menu):
        results = self._search.search_rent_orders(*values)
        search_menu = self._ui.get_search_result_menu(
            results, self.__controller_header, self.select_customer
        )
        self._menu_stack.append(search_menu)

    def go_to_create(self, values, menu):
        type_str = "pöntun"
        fields = [
            "car", "customer", "pickup_date", "pickup_time",
            "estimated_return_date", "estimated_return_time",
            "pickup_branch_name", "return_branch_name",
            "Include extra insurance (J/N)"
        ]
        new_car_menu = self._ui.get_new_model_object_menu(
            self.__controller_header, fields, type_str, self.create_order
        )
        self._menu_stack.append(new_car_menu)

    def create_order(self, values, menu):
        try:
            order = self._validation.validate_order(*values)
        except ValueError as error_msg:
            menu.set_errors((error_msg,))
            return
        self.quit()

    def create_car(self, values, menu):
        try:
            car = self._validation.validate_car(*values)
        except ValueError as error:
            menu.set_errors((error,))
            return
        self.__car_repo.add(car)
        new_car_report_menu = self._ui.get_creation_report_menu(
            car, self.__controller_header, self.restart
        )
        self._menu_stack.append(new_car_report_menu)


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