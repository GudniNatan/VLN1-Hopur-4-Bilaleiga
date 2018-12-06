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
        selection = self.handle_return_selection(selection)
        # take the selected person stored in selection,
        # make a salesperson menu,
        # add it to the menu stack
        if selection:
            salesperson_menu = self.__make_salesperson_menu(selection)
            self.__selected_salesperson = selection
            self._menu_stack.append((self.salesperson_menu, salesperson_menu))

    def salesperson_menu(self, menu):
        selection, values = menu.get_input()
        self.handle_return_selection(selection)
        if selection == 1:  # update salesperson
            # go to salesperson edit menu
            edit_menu = self.__make_edit_menu()
            self._menu_stack.append((self.edit_salesperson_menu,
                                     edit_menu))
            pass
        elif selection == 2:  # delete salesperson
            # go to deletion confirmation menu
            deletion_menu = self.__make_deletion_menu()
            self._menu_stack.append((self.delete_salesperson_menu,
                                     deletion_menu))
            pass

    def delete_salesperson_menu(self, menu):
        selection, values = menu.get_input()
        self.handle_return_selection(selection)
        if selection == 0:
            # delete the salesperson
            SalespersonRepository().remove(self.__selected_salesperson)
            # create deletion feedback menu
            # the menu should be a special no-back menu
            # go to deletion feedback screen
            delete_feedback_menu = self.__make_delete_feedback_menu()
            self.__selected_salesperson = None
            self._menu_stack.append((self.deletion_feedback_screen,
                                     delete_feedback_menu))

    def deletion_feedback_screen(self, menu):
        selection, values = menu.get_input()
        self.handle_return_selection(selection)
        if selection == 1:
            # back to salespeople main menu
            self._service.pop()
            salespeople_controller = ManageSalespeopleController(self._service)
            self._service.add(salespeople_controller)
            self._active = False

    def edit_salesperson_menu(self, menu):
        selection, values = menu.get_input()
        self.handle_return_selection(selection)
        if selection == "S":
            # Update the salesperson
            salesperson = self.__selected_salesperson
            key = salesperson.get_username()
            salesperson.set_username(values[0])
            salesperson.set_password(values[1])
            salesperson.set_name(values[2])
            salesperson.set_email(values[3])
            salesperson.set_phone(values[4])
            SalespersonRepository().update(salesperson, key)

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
        header = "Starfsmannaskrá -> Leit"
        header += "\nFann {} niðurstöður:".format(len(results))
        option_list = list()
        for person in results:
            person_option = {"description": person, "value": person}
            option_list.append(person_option)
        result_menu = Menu(header=header, options=option_list)
        return result_menu

    def __make_salesperson_menu(self, salesperson):
        name = salesperson.get_name()
        header = "Starfsmannaskrá -> Leit -> Valinn starfsmaður"
        header += "\nÞú valdir: {}".format(name)
        options = [
            {"description": "Breyta: {}".format(name)},
            {"description": "Eyða: {}".format(name)},
            ]
        return Menu(header=header, options=options)

    def __make_deletion_menu(self):
        salesperson = self.__selected_salesperson
        username = salesperson.get_username()
        header = "Starfsmannaskrá -> Leit -> Valinn starfsmaður -> Eyða"
        header += "\nErtu vissu um að þú viljir eyða {}?".format(username)
        options = [{"description": "Eyða {}".format(username), "value": 0}]
        deletion_menu = Menu(header=header, options=options)
        return deletion_menu

    def __make_delete_feedback_menu(self):
        salesperson = self.__selected_salesperson
        username = salesperson.get_name()
        header = "Starfsmannaskrá\n{} hefur verið eytt.".format(username)
        options = [{"description": "Aftur í starfsmannaskrá"}]
        delete_feedback_menu = Menu(header=header, options=options,
                                    can_go_back=False)
        return delete_feedback_menu

    def __make_edit_menu(self):
        salesperson = self.__selected_salesperson
        inputs = list()
        username = salesperson.get_username()
        header = "Starfsmannaskrá -> Leit -> Valinn starfsmaður -> Breyta"
        header += "\nSkráðu gildi fyrir {}".format(username)
        for key, value in salesperson.get_dict().items():
            input_type = "text"
            if key == "password":
                input_type = key
            input_dict = {"prompt": key, "value": value, "type": input_type}
            inputs.append(input_dict)
        edit_menu = Menu(header=header, inputs=inputs)
        return edit_menu

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
