from services.controller import Controller
from models.admin import Admin
from models.salesperson import Salesperson
from ui.menu import Menu


class MainMenuController(Controller):
    def main(self):
        user = self._service.get_current_user()
        if user is None:
            self.customer_menu()
        else:
            self.staff_menu(user)

    def customer_menu(self):
        header = "Velkominn í Bílaleigu Björgvins!"
        customer_options = [
            ("H", "Hjálp"), "Verðskrá", "Bóka bílaleigubíl",
            "Innskráning starfsmanna"
            ]
        menu = Menu(header=header, options=customer_options)
        selection, values = menu.get_input()
        print(selection)
        self.handle_return_selection(selection)
        if selection == "H":
            # create help controller, transfer control
            # and 
            pass

    def staff_menu(self, user):
        header = "Skráður inn sem {}".format(user)
        staff_options = [
            "Leigja bíl", "Skila bíl", "Birta verðlista", "Skoða pantanir",
            "Skrá viðskiptavin", "Fletta upp viðskiptavini", "Bílaskrá"
            ]
        if type(user) == Admin:
            staff_options.append("Starfsmannaskrá")