from services.controller import Controller
from repositories.salesperson_repository import SalespersonRepository
from ui.menu import Menu


class ManageSalespeopleController(Controller):
    def __init__(self, service, priority_controller=False):
        super().__init__(service, priority_controller)
        self._menu_stack.append((self.main_menu, self.__make_main_menu()))
        self.__selected_salesperson = None

    # Menus
    def main_menu(self, menu, selection, values):
        if selection == 1 or selection == 2:
            if selection == 2:
                for i in range(len(values)):
                    values[i] = ""
            results = self.__search_salespeople(*values)
            search_menu = self.__make_search_result_menu(results)
            self._menu_stack.append((self.search_result_menu, search_menu))
        elif selection == 3:
            new_salesperson_menu = self.__make_new_salesperson_menu()
            self._menu_stack.append((self.create_salesperson,
                                     new_salesperson_menu))

    def search_result_menu(self, menu, selection, values):
        # take the selected person stored in selection,
        # make a salesperson menu,
        # add it to the menu stack
        salesperson_menu = self.__make_salesperson_menu(selection)
        self.__selected_salesperson = selection
        self._menu_stack.append((self.salesperson_menu, salesperson_menu))

    def salesperson_menu(self, menu, selection, values):
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

    def delete_salesperson_menu(self, menu, selection, values):
        if selection == 0:
            # delete the salesperson
            SalespersonRepository().remove(self.__selected_salesperson)
            # create deletion feedback menu
            # the menu should be a special no-back menu
            # go to deletion feedback screen
            delete_feedback_menu = self.__make_delete_feedback_menu()
            self.__selected_salesperson = None
            self._menu_stack.append((self.feedback_screen,
                                     delete_feedback_menu))

    def edit_salesperson_menu(self, menu, selection, values):
        if selection == "S":
            # Update the salesperson
            old_salesperson = self.__selected_salesperson
            old_key = old_salesperson.get_username()
            try:
                salesperson = self._validation.validate_salesperson(*values)
            except ValueError as error:
                menu.set_errors(error)
                return
            SalespersonRepository().update(salesperson, old_key)
            # Move to feedback screen
            update_report_menu = self.__make_update_report_menu()
            self._menu_stack.append((self.feedback_screen,
                                     update_report_menu))

    def feedback_screen(self, menu, selection, values):
        # back to salespeople main menu
        self.controller_restart()

    def create_salesperson(self, menu, selection, values):
        if selection == "S":
            try:
                salesperson = self._validation.validate_salesperson(*values)
            except ValueError as error:
                menu.set_errors(error)
                return
            SalespersonRepository().add(salesperson)
            new_report_menu = self.__make_new_report_menu(salesperson)
            self._menu_stack.append((self.feedback_screen,
                                     new_report_menu))

    # Menu makers
    # Maybe move these to the UI layer?
    def __make_main_menu(self):
        header = "Starfsmannaskrá\n\nLeita af starfsmanni"
        inputs = [
            {"prompt": "Username:"}, {"prompt": "Name:"},
            {"prompt": "Email:"}, {"prompt": "Phone:"},
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

    def __make_update_report_menu(self):
        salesperson = self.__selected_salesperson
        username = salesperson.get_username()
        header = "{} hefur verið uppfærð/ur".format(username)
        return_location = "Starfsmannaskrá"
        return self.__report_menu(salesperson, header, return_location)

    def __make_new_report_menu(self, salesperson):
        username = salesperson.get_username()
        header = "{} hefur verið bætt við".format(username)
        return_location = "Starfsmannaskrá"
        return self.__report_menu(salesperson, header, return_location)

    def __report_menu(self, model_object, message, return_location):
        message += "\nNýju gildin eru:"
        for key, value in model_object.get_dict().items():
            message += "\n\t{}: {}".format(key, value)
        options = [{"description": "Aftur í {}".format(return_location)}]
        report_menu = Menu(header=message, options=options)
        return report_menu

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

    def __make_new_salesperson_menu(self):
        header = "Starfsmannaskrá -> Nýr starfsmaður"
        header += "\nSláðu inn upplýsingarnar fyrir nýja starfsmanninn:"
        inputs = [
            {"prompt": "username"},
            {"prompt": "password", "type": "password"},
            {"prompt": "name"},
            {"prompt": "email"},
            {"prompt": "phone"},
        ]
        new_salesperson_menu = Menu(header=header, inputs=inputs)
        return new_salesperson_menu

    # Other
    # These should definitely be moved somewhere else
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
