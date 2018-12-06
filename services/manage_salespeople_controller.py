from services.controller import Controller
from repositories.salesperson_repository import SalespersonRepository
from ui.menu import Menu


class ManageSalespeopleController(Controller):
    def __init__(self, service, priority_controller=False):
        super().__init__(service, priority_controller)
        self._menu_stack.append((self.main_menu, self.__make_main_menu()))
        self.__selected_salesperson = None

    # Menus
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

    def search_result_menu(self, menu):
        selection, values = menu.get_input()
        self.handle_return_selection(selection)
        # take the selected person stored in selection,
        # make a salesperson menu,
        # add it to the menu stack
        salesperson_menu = self.__make_salesperson_menu(selection)
        self.__selected_salesperson = selection
        self._menu_stack.append((self.salesperson_menu, salesperson_menu))

    def salesperson_menu(self, menu):
        selection, values = menu.get_input()
        self.handle_return_selection(selection)
        if selection == 1:  # update salesperson
            # go to salesperson edit menu
            pass
        elif selection == 2:  # delete salesperson
            # go to deletion confirmation menu
            pass

    def delete_salesperson_menu(self, menu):
        selection, values = menu.get_input()
        self.handle_return_selection(selection)
        if selection == 0:
            # delete the salesperson
            # create deletion feedback menu
            # the menu should be a special no-back menu
            # go to deletion feedback screen
            pass

    def deletion_feedback_screen(self, menu):
        selection, values = menu.get_input()
        self.handle_return_selection(selection)
        if selection == 1:
            # back to salespeople main menu
            self._service.pop()
            salespeople_controller = ManageSalespeopleController(self._service)
            self._active = False

    def edit_salesperson_menu(self, menu):
        pass

    # Menu makers
    def __make_main_menu(self):
        header = "Starfsmannaskrá\n\nLeita af starfsmanni"
        inputs = [
            {"prompt": "Notendanafn:"}, {"prompt": "Nafn:"},
            {"prompt": "Netfang:"}, {"prompt": "Símanúmer:"},
            ]
        options = [
            {"description": "Leita"}, {"description": "Sjá alla starfsmenn"},
            {"description": "Bæta við starfsmanni"},
            ]
        footer = "Sláðu inn þær upplýsingar sem þú vilt leita eftir. "
        footer += "Ekki er nauðsynlegt að fylla út alla reitina."
        menu = Menu(header=header, inputs=inputs,
                    options=options, footer=footer)
        return menu

    def __make_search_result_menu(self, results):
        header = "Starfsmannaskrá -> Leit -> Niðurstöður"
        option_list = list()
        for person in results:
            person_option = {"description": person, "value": person}
            option_list.append(person_option)
        result_menu = Menu(header=header, options=results)
        return result_menu

    def __make_salesperson_menu(self, salesperson):
        name = salesperson.get_name()
        header = "Þú valdir: {}".format(name)
        options = [
            {"description": "Breyta:".format(name)},
            {"description": "Eyða: ".format(name)},
            ]
        return Menu(header=header, options=options)

    # Other
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
