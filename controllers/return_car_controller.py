from datetime import datetime
from controllers.controller import Controller
from repositories.rent_order_repository import RentOrderRepository
from repositories.customer_repository import CustomerRepository
from ui.menu import Menu
from models.rent_order import RentOrder
from services.search import Search
from repositories.car_repository import CarRepository
from repositories.branch_repository import BranchRepository


class ReturnCarController(Controller):
    def __init__(self, service, shortcut_to_register=False,
                 priority_controller=False):
        super().__init__(service, priority_controller)
        self.__controller_header = "Skila bíl"
        self.__rent_order_repo = RentOrderRepository()
        self._menu_stack.append(self.__make_main_menu())
        self.__selected_order = None

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
        self.__selected_order = order
        extra_costs = self._utils.calculate_extra_cost(order)
        self._menu_stack.append(self.__make_order_menu(order, extra_costs))

    def close_order(self, values, menu):
        self.__selected_order.set_return_time(datetime.now())
        self.__rent_order_repo.update(self.__selected_order)
        car = self.__selected_order.get_car()
        branch_name = self.__selected_order.get_return_branch_name()
        branch = BranchRepository().get(branch_name)
        car.set_current_branch(branch)
        CarRepository().update(car)
        self._menu_stack.append(self.__make_close_order_success_menu())

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

    def __make_order_menu(self, order, extra_costs):
        total = order.get_total_cost()
        extra_insurance_price = total - order.get_base_cost()
        already_payed_amount = total - order.get_remaining_debt()
        extra_cost_total = sum([cost["amount"] for cost in extra_costs])
        extra_cost_str = "\n\t".join(
            (cost["name"] + ": " + str(cost["amount"]) for cost in extra_costs)
        )
        if not extra_cost_str:
            extra_cost_str = "Enginn"
        remaining = order.get_remaining_debt() + extra_cost_total
        header = "".join((
            self.__controller_header, " -> Leit -> Valin pöntun",
            "Pöntun númer: ", str(order.get_order_number()),
            "\nUpphafstími leigu: ", str(order.get_pickup_time()),
            "\nÁætlaður skilatími: ", str(order.get_estimated_return_time()),
            "\nTegund bíls: ", order.get_car().get_name(),
            "\nNafn leigjanda: ", order.get_customer().get_name(),
            "\n\nGrunnverð: ", str(order.get_base_cost()), " kr.",
            "\nAukatrygging: ", str(extra_insurance_price), " kr.",
            "\nViðbættur kostnaður: ", extra_cost_str,
            "\nHeildarkostnaður: ", str(total), " kr.",
            "\n\nÁður greitt: ", str(already_payed_amount), " kr."
            "\nEftirstöður ", str(remaining), " kr."
        ))
        options = [
            {"description": "Borga núna og loka pöntun",
                "value": self.close_order}
        ]
        return Menu(
            header=header, options=options, back_function=self.back,
            stop_function=self.stop,
        )

    def __make_close_order_success_menu(self):
        header = "".join((
            "Skila bíl -> Leit -> Valin pöntun -> Lokið\n\n"
            "Pöntunin þín er lokuð. ",
            "\n\n\nTakk fyrir að velja Bílaleigu Björgvins!\n"
        ))
        return Menu(
            header=header, stop_function=self.stop, can_go_back=False
        )
