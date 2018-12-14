from controllers.controller import Controller
from models.admin import Admin
from models.salesperson import Salesperson
from ui.menu import Menu
from controllers.help_menu_controller import HelpMenuController
from controllers.manage_salespeople_controller import ManageSalespeopleController
from controllers.manage_customers_controller import ManageCustomersController
from controllers.manage_cars_controller import ManageCarsController
from controllers.manage_orders_controller import ManageOrdersController
from controllers.price_list_controller import PriceListController
from controllers.rent_car_controller import RentCarController
from controllers.return_car_controller import ReturnCarController


class MainMenuController(Controller):
    def __init__(self, service, priority_controller=True):
        super().__init__(service, priority_controller)
        # always append the first active menu function in the constructor
        # Usually, this should also call a make menu function.
        self._menu_stack.append(self.__make_customer_menu())

    # Operations
    def go_to_help_controller(self, values, menu):
        help_controller = HelpMenuController(self._service)
        self._service.add(help_controller)

    def go_to_price_list_controller(self, values, menu):
        price_list_controller = PriceListController(self._service)
        self._service.add(price_list_controller)

    def go_to_login(self, values, menu):
        self._menu_stack.append(self.__make_login_menu())

    def log_out(self, values, menu):
        self._service.set_current_user(None)
        self.restart()

    def go_to_salespeople_controller(self, values, menu):
        salespeople_controller = ManageSalespeopleController(self._service)
        self._service.add(salespeople_controller)

    def go_to_customer_controller(self, values, menu):
        customer_controller = ManageCustomersController(self._service)
        self._service.add(customer_controller)

    def go_to_car_controller(self, values, menu):
        car_controller = ManageCarsController(self._service)
        self._service.add(car_controller)

    def go_to_order_controller(self, value, menu):
        order_controller = ManageOrdersController(self._service)
        self._service.add(order_controller)

    def go_to_add_customer(self, values, menu):
        customer_controller = ManageCustomersController(
            self._service, shortcut_to_register=True
        )
        self._service.add(customer_controller)

    def go_to_rent_car_controller(self, values, menu):
        rent_car_controller = RentCarController(self._service)
        self._service.add(rent_car_controller)

    def go_to_return_car_controller(self, values, menu):
        return_car_controller = ReturnCarController(self._service)
        self._service.add(return_car_controller)

    def handle_login(self, values, menu):
        try:
            user = self._validation.validate_login(*values)
        except ValueError as error_str:
            menu.set_errors((error_str,))
            return
        except FileNotFoundError as error_str:
            menu.set_errors((error_str,))
            return
        self._service.set_current_user(user)
        self._menu_stack[0] = self.__make_staff_menu()
        self.back()

    # Menu makers
    # Maybe move these to the UI layer?
    def __make_customer_menu(self):
        header = "Velkominn í Bílaleigu Björgvins!"
        go_to_help = self.go_to_help_controller
        go_to_price_list = self.go_to_price_list_controller
        go_to_login = self.go_to_login
        go_to_rent_car = self.go_to_rent_car_controller
        customer_options = [
            {"hotkey": "H", "description": "Hjálp", "value": go_to_help},
            {"description": "Verðskrá", "value": go_to_price_list},
            {"description": "Bóka bílaleigubíl", "value": go_to_rent_car},
            {"description": "Innskráning starfsmanna", "value": go_to_login},
        ]
        footer = "Notaðu örvatakkana til að hreyfa bendilinn. "
        footer += "Notaðu enter til að velja."
        menu = Menu(header=header, options=customer_options, can_go_back=False,
                    footer=footer, stop_function=self.stop, full_quit=True)
        return menu

    def __make_staff_menu(self):
        user = self._service.get_current_user()
        header = "Skráður inn sem {}\n".format(type(user).__name__)
        header += "Velkomin/n aftur, {}!".format(user.get_name())
        staff_options = [
            {"description": "Leigja bíl",
                "value": self.go_to_rent_car_controller},
            {"description": "Skila bíl",
                "value": self.go_to_return_car_controller},
            {"description": "Verðskrá",
                "value": self.go_to_price_list_controller},
            {"description": "Skrá viðskiptavin",
                "value": self.go_to_add_customer},
            {"description": "Fletta upp viðskiptavini",
                "value": self.go_to_customer_controller},
            {"description": "Pantanaskrá",
                "value": self.go_to_order_controller},
            {"description": "Bílaskrá",
                "value": self.go_to_car_controller},
            {"hotkey": 'X', "description": "Skrá út", "value": self.log_out}
        ]
        if type(user) == Admin:
            staff_op = {"description": "Starfsmannaskrá",
                        "value": self.go_to_salespeople_controller}
            staff_options.insert(-1, staff_op)
        menu = Menu(header=header, options=staff_options, can_go_back=False,
                    stop_function=self.stop, max_options_per_page=12,
                    full_quit=True)
        return menu

    def __make_login_menu(self):
        header = "Innskráning starfsmanna:"
        inputs = [
            {"prompt": "Notendanafn: "},
            {"prompt": "Lykilorð: ", "type": "password"}
        ]
        login_menu = Menu(
            header=header, inputs=inputs, stop_function=self.stop,
            submit_function=self.handle_login, back_function=self.back,
            full_quit=True
        )
        return login_menu
