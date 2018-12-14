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
        self.__selected_car = None

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
        self._menu_stack.append(self.__make_ask_km(order))

    def calculate_costs(self, values, menu):
        self.__selected_car = self.__selected_order.get_car()
        try:
            new_km_count = self._validation.validate_kilometer_driven(
                values[0], self.__selected_car
            )
        except ValueError as error_msg:
            menu.set_errors([error_msg])
            return
        old_km_count = self.__selected_car.get_kilometer_count()
        self.__selected_car.set_kilometer_count(new_km_count)
        driven_km = new_km_count - old_km_count
        self.__selected_order.set_kilometers_driven(driven_km)
        extra_costs = self._utils.calculate_extra_cost(self.__selected_order)
        self._menu_stack.append(self.__make_order_menu(self.__selected_order,
                                                       extra_costs))

    def close_order(self, values, menu):
        self.__selected_order.set_return_time(datetime.now())
        self.__rent_order_repo.update(self.__selected_order)
        branch_name = self.__selected_order.get_return_branch_name()
        branch = BranchRepository().get(branch_name)
        self.__selected_car.set_current_branch(branch)
        CarRepository().update(self.__selected_car)
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

    def __make_ask_km(self, order):
        car = order.get_car()
        header = "".join((
            self.__controller_header, " -> Leit -> Valin pöntun",
            "Pöntun númer: ", str(order.get_order_number()),
            "\nUpphafstími leigu: ", str(order.get_pickup_time()),
            "\nÁætlaður skilatími: ", str(order.get_estimated_return_time()),
            "\nTegund bíls: ", order.get_car().get_name(),
            "\nNafn leigjanda: ", order.get_customer().get_name(),
            "\n\nNúverandi kílómetrafjöldi á bílnum: ",
            str(car.get_kilometer_count())
        ))
        inputs = [
            {"prompt": "Sláðu inn nýjan kílómetrafjölda"}
        ]
        return Menu(
            header=header, inputs=inputs, back_function=self.back,
            stop_function=self.stop, submit_function=self.calculate_costs
        )

    def __make_order_menu(self, order, extra_costs):
        total = order.get_total_cost()
        extra_insurance_price = total - order.get_base_cost()
        already_payed_amount = total - order.get_remaining_debt()
        already_payed_amount += order.get_addon_price()
        extra_cost_total = sum([cost["amount"] for cost in extra_costs])
        cost_str_list = list()
        for cost in extra_costs:
            cost_str_list.append(
                cost["name"] + ": " + str(cost["amount"]) + " kr."
            )
        extra_cost_str = "\n\t".join(cost_str_list)
        if not extra_cost_str:
            extra_cost_str = "Enginn"
        remaining = order.get_remaining_debt() + extra_cost_total
        header = "".join((
            self.__controller_header, " -> Leit -> Valin pöntun",
            "\nPöntun númer: ", str(order.get_order_number()),
            "\nUpphafstími leigu: ", str(order.get_pickup_time()),
            "\nÁætlaður skilatími: ", str(order.get_estimated_return_time()),
            "\nTegund bíls: ", order.get_car().get_name(),
            "\nNafn leigjanda: ", order.get_customer().get_name(),
            "\n\nGrunnverð: ", str(order.get_base_cost()), " kr.",
            "\nAukatrygging: ", str(extra_insurance_price), " kr.",
            "\nVerð á aukahlutum: ", str(order.get_addon_price()),
            "\nViðbættur kostnaður: ", extra_cost_str, " kr.",
            "\nHeildarkostnaður: ", str(total), " kr.",
            "\n\nÁður greitt: ", str(already_payed_amount), " kr."
            "\nEftirstöður ", str(remaining), " kr."
        ))
        if remaining != 0:
            options = [
                {"description": "Borga núna og loka pöntun",
                    "value": self.close_order}
            ]
        else:
            options = [
                {"description": "Skila bíl og loka pöntun",
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
