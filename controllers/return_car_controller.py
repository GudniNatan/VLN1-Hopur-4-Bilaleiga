from controllers.controller import Controller
from repositories.rent_order_repository import RentOrderRepository
from repositories.customer_repository import CustomerRepository
from ui.menu import Menu
from models.rent_order import RentOrder
from services.search import Search


class ReturnCarController(Controller):
    def __init__(self, service, shortcut_to_register=False,
                 priority_controller=False):
        super().__init__(service, priority_controller)
        self.__controller_header = "Skila bíl"
        self.__rent_order_repo = RentOrderRepository()
        self._menu_stack.append(self.__make_main_menu())

    def search(self, values, menu):
        drivers_license_id = values[0]
        try:
            customer = CustomerRepository().get(drivers_license_id)
        except ValueError:
            error_msg = "Enginn viðskiptavinur með þetta "
            error_msg += "ökuskírteinisnúmer fannst"
            menu.set_errors((error_msg,))
            return
        results = self._search.search_rent_orders(
            customer=customer.get_key(), active=True
        )
        if not results:
            error_msg = "\n".join((
                "Fann virkar opnar pantanir hjá þessum viðskiptavini " +
                "(" + customer.get_name() + ")",
                "Ef þú vilt bakfæra óvirka pöntun er hægt að gera það" +
                " gegnum pantanaskránna."
            ))
            menu.set_errors((error_msg,))
            return
        menu = self._ui.get_search_result_menu(
            results, self.__controller_header, self.select_order
        )
        self._menu_stack.append(menu)

    def select_order(self, order, menu):
        pass

    def __make_main_menu(self):
        header = "".join((
            self.__controller_header,
            "\n\nSláðu inn ökuskírteinisnúmer hjá viðskiptavini.",
            " Þá er hægt að velja pöntunina fyrir þann bíl sem var skilað.",
        ))
        
        inputs = [
            {"prompt": "Ökuskírteinisnúmer viðskiptavinar:"}
        ]
        options = [{"description": "Sjá opnar pantanir",
                   "value": self.search}]
        return Menu(
            header=header, options=options, back_function=self.back,
            stop_function=self.stop, can_submit=False, inputs=inputs
        )