from services.controller import Controller
from models.admin import Admin
from models.salesperson import Salesperson
from ui.menu import Menu
from services.help_menu_controller import HelpMenuController
from services.manage_salespeople_controller import ManageSalespeopleController


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

    def go_to_login(self, values, menu):
        self._menu_stack.append(self.__make_login_menu())

    def log_out(self, values, menu):
        self._service.set_current_user(None)
        self.restart()

    def go_to_salespeople_controller(self, values, menu):
        salespeople_controller = ManageSalespeopleController(self._service)
        self._service.add(salespeople_controller)

    def handle_login(self, values, menu):
        user = self._validation.validate_login(*values)
        self._service.set_current_user(user)
        if user is None:
            menu.set_errors(("Rangt notendanafn eða lykilorð.",))
        else:
            self._menu_stack[0] = self.__make_staff_menu()
            self.back()

    # Menu makers
    # Maybe move these to the UI layer?
    def __make_customer_menu(self):
        header = "Velkominn í Bílaleigu Björgvins!"
        help_function = self.go_to_help_controller
        go_to_login = self.go_to_login
        customer_options = [
            {"hotkey": "H", "description": "Hjálp", "value": help_function},
            {"description": "Verðskrá"},
            {"description": "Bóka bílaleigubíl"},
            {"description": "Innskráning starfsmanna", "value": go_to_login},
            ]
        footer = "Notaðu örvatakkana til að hreyfa bendilinn. "
        footer += "Notaðu enter til að velja."
        menu = Menu(header=header, options=customer_options, can_go_back=False,
                    footer=footer, stop_function=self.stop)
        return menu

    def __make_staff_menu(self):
        user = self._service.get_current_user()
        header = "Skráður inn sem {}\n".format(type(user))
        header += "Velkomin/n aftur, {}!".format(user.get_name())
        staff_options = [
            {"description": "Leigja bíl"},
            {"description": "Skila bíl"},
            {"description": "Birta verðlista"},
            {"description": "Skoða pantanir"},
            {"description": "Skrá viðskiptavin"},
            {"description": "Fletta upp viðskiptavini"},
            {"description": "Bílaskrá"},
            {"hotkey": 'X', "description": "Skrá út", "value": self.log_out}
            ]
        if type(user) == Admin:
            staff_op = {"description": "Starfsmannaskrá",
                        "value": self.go_to_salespeople_controller}
            staff_options.insert(-1, staff_op)
        menu = Menu(header=header, options=staff_options, can_go_back=False,
                    stop_function=self.stop)
        return menu

    def __make_login_menu(self):
        header = "Innskráning starfsmanna:"
        inputs = [
            {"prompt": "Notendanafn: "},
            {"prompt": "Lykilorð: ", "type": "password"}
        ]
        login_menu = Menu(
            header=header, inputs=inputs, stop_function=self.stop,
            submit_function=self.handle_login, back_function=self.back
            )
        return login_menu
