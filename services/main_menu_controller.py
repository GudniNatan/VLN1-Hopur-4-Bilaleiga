from services.controller import Controller
from models.admin import Admin
from models.salesperson import Salesperson
from ui.menu import Menu
from services.help_menu_controller import HelpMenuController
from services.manage_salespeople_controller import ManageSalespeopleController


class MainMenuController(Controller):
    def __init__(self, service, priority_controller=True):
        super().__init__(service, priority_controller)
        self._menu_stack.append((self.main_menu, None))

    def main_menu(self, values):
        user = self._service.get_current_user()
        if user is None:
            self.customer_menu()
        else:
            self.staff_menu(user)

    def customer_menu(self):
        header = "Velkominn í Bílaleigu Björgvins!"
        customer_options = [
            {"hotkey": "H", "description": "Hjálp"},
            {"description": "Verðskrá"},
            {"description": "Bóka bílaleigubíl"},
            {"description": "Innskráning starfsmanna"},
            ]
        menu = Menu(header=header, options=customer_options, can_go_back=False)
        selection, values = menu.get_input()
        self.handle_return_selection(selection)
        if selection == "H":
            # create help controller, transfer control
            help_controller = HelpMenuController(self._service)
            self._service.add(help_controller)
            self._active = False
        if selection == 3:
            self._menu_stack.append((self.login, self.make_login_menu()))

    def staff_menu(self, user):
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
            {"hotkey": 'X', "description": "Skrá út"}
            ]
        if type(user) == Admin:
            staff_options.insert(-1, {"description": "Starfsmannaskrá"})
        menu = Menu(header=header, options=staff_options, can_go_back=False)
        selection, values = menu.get_input()
        self.handle_return_selection(selection)
        if selection == "X":
            self._service.set_current_user(None)
        elif selection == 8:
            salespeople_controller = ManageSalespeopleController(self._service)
            self._service.add(salespeople_controller)
            self._active = False

    def make_login_menu(self):
        header = "Innskráning starfsmanna:"
        inputs = [
            {"prompt": "Notendanafn: "},
            {"prompt": "Lykilorð: ", "type": "password"}
        ]
        login_menu = Menu(header=header, inputs=inputs)
        return login_menu

    def login(self, login_menu=None):
        if not login_menu:
            login_menu = self.make_login_menu()
        selection, values = login_menu.get_input()
        self.handle_return_selection(selection)
        if selection == "S":
            user = self._validation.validate_login(*values)
            self._service.set_current_user(user)
            if user is None:
                login_menu.set_errors(("Rangt notendanafn eða lykilorð.",))
            else:
                self._menu_stack.pop()
