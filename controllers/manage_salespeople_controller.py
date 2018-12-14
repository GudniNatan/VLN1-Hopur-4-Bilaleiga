from controllers.controller import Controller
from repositories.salesperson_repository import SalespersonRepository
from ui.menu import Menu


class ManageSalespeopleController(Controller):
    def __init__(self, service, priority_controller=False):
        super().__init__(service, priority_controller)
        self._menu_stack.append(self.__make_main_menu())
        self.__selected_salesperson = None
        self.__controller_header = "Starfsmannaskrá"

    # Operations
    def go_to_search(self, values, menu):
        results = self._search.search_salespeople(*values)
        search_menu = self._ui.get_search_result_menu(
            results, self.__controller_header, self.select_person
            )
        self._menu_stack.append(search_menu)

    def go_to_search_all(self, values, menu):
        for i in range(len(values)):
            values[i] = ""
        self.go_to_search(values, menu)

    def go_to_create(self, values, menu):
        new_salesperson_menu = self.__make_new_salesperson_menu()
        self._menu_stack.append(new_salesperson_menu)

    def create_person(self, values, menu):
        try:
            salesperson = self._validation.validate_salesperson(*values)
        except ValueError as error:
            menu.set_errors((error,))
            return
        SalespersonRepository().add(salesperson)
        new_report_menu = self._ui.get_creation_report_menu(
            salesperson, self.__controller_header, self.restart
        )
        self._menu_stack.append(new_report_menu)

    def select_person(self, salesperson, menu):
        salesperson_menu = self._ui.get_model_object_options_menu(
            salesperson, salesperson.get_name(), self.__controller_header,
            self.go_to_edit, self.go_to_delete
        )
        self.__selected_salesperson = salesperson
        self._menu_stack.append(salesperson_menu)

    def go_to_edit(self, values, menu):
        salesperson = self.__selected_salesperson
        name = salesperson.get_name()
        edit_menu = self._ui.get_edit_menu(
            salesperson, name, self.__controller_header, self.edit_person
        )
        self._menu_stack.append(edit_menu)

    def edit_person(self, values, menu):
        # Update the salesperson
        old_salesperson = self.__selected_salesperson
        old_key = old_salesperson.get_username()
        try:
            salesperson = self._validation.validate_salesperson(*values)
        except ValueError as error:
            menu.set_errors((error,))
            return
        SalespersonRepository().update(salesperson, old_key)
        # Move to feedback screen
        update_report_menu = self._ui.get_edit_report_menu(
            salesperson, self.__controller_header, self.restart
        )
        self._menu_stack.append(update_report_menu)

    def go_to_delete(self, value, menu):
        salesperson = self.__selected_salesperson
        deletion_menu = self._ui.get_deletion_menu(
            salesperson, salesperson.get_name(), self.__controller_header,
            self.delete_selected_person
        )
        self._menu_stack.append(deletion_menu)

    def delete_selected_person(self, value, menu):
        # delete the salesperson
        SalespersonRepository().remove(self.__selected_salesperson)
        # create deletion feedback menu
        # the menu should be a special no-back menu
        # go to deletion feedback screen
        delete_feedback_menu = self._ui.get_delete_feedback_menu(
            self.__selected_salesperson.get_name(),
            self.__controller_header, self.restart
        )
        self.__selected_salesperson = None
        self._menu_stack.append(delete_feedback_menu)

    # Menu makers
    def __make_main_menu(self):
        header = "Starfsmannaskrá\n\nLeita að starfsmanni"
        inputs = [
            {"prompt": "Username:"}, {"prompt": "Name:"},
            {"prompt": "Email:"}, {"prompt": "Phone:"},
        ]
        search = self.go_to_search
        search_all = self.go_to_search_all
        create = self.go_to_create
        options = [
            {"description": "Leita", "value": search},
            {"description": "Sjá alla starfsmenn", "value": search_all},
            {"description": "Bæta við starfsmanni", "value": create},
        ]
        footer = "Sláðu inn þær upplýsingar sem þú vilt leita eftir. "
        footer += "Ekki er nauðsynlegt að fylla út alla reitina."
        menu = Menu(header=header, inputs=inputs,
                    options=options, footer=footer, can_submit=False,
                    back_function=self.back, stop_function=self.stop)
        return menu

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
        new_salesperson_menu = Menu(header=header, inputs=inputs,
                                    back_function=self.back,
                                    stop_function=self.stop,
                                    submit_function=self.create_person)
        return new_salesperson_menu
