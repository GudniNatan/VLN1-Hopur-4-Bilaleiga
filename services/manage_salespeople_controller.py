from services.controller import Controller
from repositories.salesperson_repository import SalespersonRepository
from ui.menu import Menu


class ManageSalespeopleController(Controller):
    def __init__(self, service, priority_controller=False):
        super().__init__(service, priority_controller)
        self._menu_stack.append((self.main_menu, self.__make_main_menu()))

    def __make_main_menu(self):
        header = "Starfsmannaskrá\n\nLeita af starfsmanni"
        inputs = [
            {"prompt": "Notendanafn:"},
            {"prompt": "Nafn:"},
            {"prompt": "Netfang:"},
            {"prompt": "Símanúmer:"},
            ]
        options = ["Leita", "Sjá alla starfsmenn", "Bæta við starfsmanni"]
        footer = "Sláðu inn þær upplýsingar sem þú vilt leita eftir. "
        footer += "Ekki er nauðsynlegt að fylla út alla reitina."
        menu = Menu(header=header, inputs=inputs,
                    options=options, footer=footer)
        return menu

    def main_menu(self, menu):
        selection, values = menu.get_input()
        self.handle_return_selection(selection)
        if selection == 1 or selection == 2:
            if selection == 2:
                for i in range(len(values)):
                    values[i] == ""
            results = self.__search_salespeople(*values)
            search_menu = self.__make_search_result_menu(results)
            self._menu_stack.append((self.search_result_menu, search_menu))

    def __make_search_result_menu(self, results):
        header = "Starfsmannaskrá -> Leit -> Niðurstöður"
        result_menu = Menu(header=header, options=results)
        return result_menu

    def __search_salespeople(self, username="", name="", email="", phone=""):
        salespeople = SalespersonRepository().get_all()
        username = username.strip()
        name = name.strip()
        email = email.strip()
        phone = phone.strip()
        for i in range(len(salespeople) - 1, -1, -1):
            person = salespeople[i]
            if username and username != person.get_username():
                salespeople.pop(i)
            elif name and name != person.get_name():
                salespeople.pop(i)
            elif email and email != person.get_email():
                salespeople.pop(i)
            elif phone and phone != person.get_phone():
                salespeople.pop(i)
        return salespeople

    def search_result_menu(self, menu):
        selection, values = menu.get_input()
        self.handle_return_selection(selection)
        # take the selected person stored in selection and
        # make a salesperson menu
