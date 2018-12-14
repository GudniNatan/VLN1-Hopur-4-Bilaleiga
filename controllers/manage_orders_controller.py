from collections import OrderedDict
from controllers.controller import Controller
from repositories.rent_order_repository import RentOrderRepository
from ui.menu import Menu
from models.admin import Admin


class ManageOrdersController(Controller):
    def __init__(self, service, shortcut_to_register=False,
                 priority_controller=False):
        super().__init__(service, priority_controller)
        self.__controller_header = "Pantanaskrá"
        self.__order_repo = RentOrderRepository()
        self.__selected_order = None
        self._menu_stack.append(self.__make_main_menu())

    # Operations
    def go_to_search(self, values, menu):
        results = self._search.search_rent_orders(*values)
        search_menu = self._ui.get_search_result_menu(
            results, self.__controller_header, self.select_order
        )
        self._menu_stack.append(search_menu)

    def select_order(self, order, menu):
        order_menu = self._ui.get_model_object_options_menu(
            order, order.get_key(), self.__controller_header,
            self.go_to_edit, self.go_to_delete
        )
        self.__selected_order = order
        self._menu_stack.append(order_menu)

    def go_to_edit(self, values, menu):
        order = self.__selected_order
        name = order.get_name()
        est_return_datetime = order.get_estimated_return_time()
        extra_insurance_str = "J"
        if order.get_extra_insurance_total != 0:
            extra_insurance_str = "N"
        fields = OrderedDict([
            ("Bílnúmer",  order.get_car().get_key()),
            ("Ökuskírteinisnúmer", order.get_customer().get_key()),
            ("Sótt (dagssetning)", order.get_pickup_time().date()),
            ("Sótt (klukkan)", order.get_pickup_time().time()),
            ("Áætluð skiladagssetning", est_return_datetime.date()),
            ("Áætlaður skilatími", est_return_datetime.time()),
            ("Sótt hjá", order.get_pickup_branch_name()),
            ("Skilað hjá", order.get_return_branch_name()),
            ("Inniheldur auka tryggingu (J/N)", extra_insurance_str)
        ])

        edit_menu = self._ui.get_edit_by_field_menu(
            fields, name, self.__controller_header, self.edit_selected_order
        )
        self._menu_stack.append(edit_menu)

    def go_to_create(self, values, menu):
        type_str = "pöntun"
        order = self.__selected_order
        fields = [
            "Bílnúmer", "Ökuskírteinisnúmer Viðskiptavinur",
            "Dagsetning sótt", "Sótt klukkan", "Áætluð skiladagssetning",
            "Áætlaður skilatími", "Sótt í útibúi", "Skilað í útibúi",
            "Inniheldur auka tryggingu (J/N)"
        ]
        new_car_menu = self._ui.get_new_model_object_menu(
            self.__controller_header, fields, type_str, self.create_order
        )
        self._menu_stack.append(new_car_menu)

    def create_order(self, values, menu):
        try:
            order = self._validation.validate_order(*values)
        except ValueError as error_msg:
            menu.set_errors((error_msg,))
            return
        self.__order_repo.add(order)
        new_order_report_menu = self._ui.get_creation_report_menu(
            order, self.__controller_header, self.restart
        )
        self._menu_stack.append(new_order_report_menu)

    def go_to_delete(self, values, menu):
        order = self.__selected_order
        deletion_menu = self._ui.get_deletion_menu(
            order, order.get_name(), self.__controller_header,
            self.delete_selected_order
        )
        self._menu_stack.append(deletion_menu)

    def edit_selected_order(self, values, menu):
        # Update the order
        old_order = self.__selected_order
        old_key = old_order.get_key()
        try:
            order = self._validation.validate_order(
                *values, order_number=old_key
            )
        except ValueError as error:
            menu.set_errors((error,))
            return
        self.__order_repo.update(order, old_key)
        # Move to feedback screen
        update_report_menu = self._ui.get_edit_report_menu(
            order, self.__controller_header, self.restart
        )
        self._menu_stack.append(update_report_menu)

    def delete_selected_order(self, values, menu):
        self.__order_repo.remove(self.__selected_order)
        delete_feedback_menu = self._ui.get_delete_feedback_menu(
            self.__selected_order.get_name(),
            self.__controller_header, self.restart
        )
        self.__selected_order = None
        self._menu_stack.append(delete_feedback_menu)

    def __make_main_menu(self):
        header = self.__controller_header
        header += "\n\nLeita að pöntun"
        inputs = [{"prompt": "Pöntunarnúmer:"},
                  {"prompt": "Kennitala viðskiptarvinar:"},
                  {"prompt": "Bílnúmer:"},
                  {"prompt": "Fela óvirkar pantanir (J/N):"}]
        search = self.go_to_search
        search_all = self.go_to_search_all
        create = self.go_to_create
        options = [
            {"description": "Leita", "value": search},
            {"description": "Sjá allar pantanir", "value": search_all},
            {"description": "Bæta við pöntun", "value": create}
        ]
        footer = "Sláðu inn þær upplýsingar sem þú vilt leita eftir. "
        footer += "Ekki er nauðsynlegt að fylla út alla reitina."
        menu = Menu(
            header=header, inputs=inputs, options=options, footer=footer,
            can_submit=False, back_function=self.back, stop_function=self.stop,
            max_options_per_page=10
        )
        return menu
