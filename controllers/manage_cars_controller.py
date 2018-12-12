from controllers.controller import Controller
from repositories.car_repository import CarRepository
from ui.menu import Menu
from models.admin import Admin
from services.search import Search


class ManageCarsController(Controller):
    def __init__(self, service, shortcut_to_register=False,
                 priority_controller=False):
        super().__init__(service, priority_controller)
        self.__controller_header = "Bílaskrá"
        self.__car_repo = CarRepository()
        self.__selected_car = None
        self._menu_stack.append(self.__make_main_menu())

    # Operations
    def go_to_search(self, values, menu):
        results = Search().search_cars(*values)
        search_menu = self._ui.get_search_result_menu(
            results, self.__controller_header, self.select_car
        )
        self._menu_stack.append(search_menu)

    def go_to_create(self, values, menu):
        type_str = "Bílinn"
        fields = [
            "license_plate_number", "model", "category", "wheel_count",
            "drivetrain", "automatic_transmission (J/N)", "seat_count",
            "extra_properties (comma seperated)", "kilometer_count"
        ]
        new_car_menu = self._ui.get_new_model_object_menu(
            self.__controller_header, fields, type_str, self.create_car
        )
        self._menu_stack.append(new_car_menu)

    def select_car(self, car, menu):
        car_menu = self._ui.get_model_object_options_menu(
            car, car.get_license_plate_number(), self.__controller_header,
            self.go_to_edit, self.go_to_delete
        )
        self.__selected_car = car
        self._menu_stack.append(car_menu)

    def go_to_edit(self, values, menu):
        car = self.__selected_car
        name = car.get_license_plate_number()
        edit_menu = self._ui.get_edit_menu(
            car, name, self.__controller_header, self.edit_car
        )
        self._menu_stack.append(edit_menu)

    def edit_selected_car(self, values, menu):
        # Update the salesperson
        old_customer = self.__selected_customer
        old_key = old_customer.get_drivers_license_id()
        try:
            customer = self._validation.validate_customer(*values)
        except ValueError as error:
            menu.set_errors((error,))
            return
        self.__customer_repo.update(customer, old_key)
        # Move to feedback screen
        update_report_menu = self._ui.get_edit_report_menu(
            customer, self.__controller_header, self.restart
        )
        self._menu_stack.append(update_report_menu)

    def go_to_delete(self, values, menu):
        pass

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

    # Menus - try to move these to the ui layer
    def __make_main_menu(self):
        header = self.__controller_header
        header += "\n\nLeita að bíl"
        inputs = [{"prompt": "Númeraplata:"},
                  {"prompt": "Flokkur:"},
                  {"prompt": "Fjöldi sæta:"},
                  {"prompt": "Sjálfskiptur (J/N):"},
                  {"prompt": "Fela lausa bíla (J/N):"},
                  {"prompt": "Fela leigða bíla (J/N):"}]
        search = self.go_to_search
        search_all = self.go_to_search_all
        create = self.go_to_create
        options = [
            {"description": "Leita", "value": search},
            {"description": "Sjá alla bíla", "value": search_all},
        ]
        if type(self._service.get_current_user()) == Admin:
            add_car_option = {"description": "Bæta við bíl", "value": create}
            options.append(add_car_option)
        footer = "Sláðu inn þær upplýsingar sem þú vilt leita eftir. "
        footer += "Ekki er nauðsynlegt að fylla út alla reitina."
        menu = Menu(
            header=header, inputs=inputs, options=options, footer=footer,
            can_submit=False, back_function=self.back, stop_function=self.stop,
            max_options_per_page=10
        )
        return menu
