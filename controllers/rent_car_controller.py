from controllers.controller import Controller
from repositories.car_repository import CarRepository
from repositories.branch_repository import BranchRepository
from repositories.price_list_repository import PriceListRepository
from repositories.customer_repository import CustomerRepository
from repositories.rent_order_repository import RentOrderRepository
from controllers.manage_customers_controller import ManageCustomersController
from ui.menu import Menu
from models.rent_order import RentOrder
from services.search import Search


class RentCarController(Controller):
    def __init__(self, service, shortcut_to_register=False,
                 priority_controller=False):
        super().__init__(service, priority_controller)
        self.__controller_header = "Leigja bíl"
        self.__car_repo = CarRepository()
        self.__price_list_repo = PriceListRepository()
        self.__customer_repo = CustomerRepository()
        self._menu_stack.append(self.__make_main_menu())
        self.__selected_date_range = None
        self.__selected_category = None
        self.__selected_pickup_branch = None
        self.__selected_return_branch = None
        self.__selected_car = None
        self.__selected_customer = None
        self.__include_insurance = False
        self.__order = None

    def submit_time_period(self, values, menu):
        from_date = values[0:2]
        to_date = values[2:4]
        try:
            date_range = self._validation.validate_rent_range(
                from_date, to_date
            )
        except ValueError as error_msg:
            menu.set_errors((error_msg,))
            return
        self.__selected_date_range = date_range
        self._menu_stack.append(self.__make_category_option_menu())

    def go_to_pickup_branch_choice(self, category, menu):
        category = category.split(":")[0]
        self.__selected_category = self.__price_list_repo.get(category)
        self._menu_stack.append(self.__make_branch_option_menu())

    def go_to_return_branch_choice(self, branch, menu):
        self.__selected_pickup_branch = branch
        self._menu_stack.append(self.__make_branch_option_menu(True))

    def go_to_search(self, branch, menu):
        self.__selected_return_branch = branch
        from_date, to_date = self.__selected_date_range
        results = self._search.search_cars(
            category=self.__selected_category,
            availability_lower_bound=from_date,
            availability_upper_bound=to_date,
            in_branch=self.__selected_pickup_branch,
            hide_unavailable=True
        )
        self._menu_stack.append(self._ui.get_search_result_menu(
            results, self.__controller_header, self.choose_car
        ))

    def choose_car(self, car, menu):
        self.__selected_car = car
        self._menu_stack.append(self.__make_extra_insurance_menu())

    def get_insurance(self, values, menu):
        self.__include_insurance = True
        self._menu_stack.append(self.__make_customer_select_menu())

    def skip_insurance(self, values, menu):
        self.__include_insurance = False
        self._menu_stack.append(self.__make_customer_select_menu())

    def log_in(self, values, menu):
        driver_license_id = values[0]
        try:
            customer = self.__customer_repo.get(driver_license_id)
        except ValueError:
            error_msg = "".join((
                "Enginn viðskiptavinur með þetta ökuskírteinisnúmer ",
                "fannst. Ertu örugglega skráð/ur?\n"
            ))
            menu.set_errors((error_msg,))
            return
        self.__selected_customer = customer
        self.create_order()

    def register(self, values, menu):
        customer_controller = ManageCustomersController(
            self._service, shortcut_to_register=True, rent=True
        )
        self._service.add(customer_controller)

    def create_order(self, values=None, menu=None):
        car = self.__selected_car
        customer = self.__selected_customer
        date_range = self.__selected_date_range
        pickup_branch = self.__selected_pickup_branch
        return_branch = self.__selected_return_branch
        try:
            order = self._validation.assemble_order(
                car, customer, date_range, pickup_branch, return_branch,
                self.__include_insurance,
            )
            self.__order = order
        except ValueError as error_msg:
            menu.set_errors((error_msg),)
            return
        self._menu_stack.append(self.__make_order_report_menu(order))

    def pay_now(self, values, menu):
        self.__order.set_remaining_debt(0)
        self.pay_later()

    def pay_later(self, values=None, menu=None):
        RentOrderRepository().add(self.__order)
        self._menu_stack.append(self.__make_order_success_menu())

    def __make_main_menu(self):
        header = " ".join((
            self.__controller_header + " -> Leigutímabil",
            "\nHér er hægt að leigja bíl.",
            "Byrjaðu á því að velja leigutímabil"
        ))
        inputs = [
            {"prompt": "Upphafsdagsetning (DD/MM/ÁÁÁÁ):"},
            {"prompt": "Upphafstími (KK:MM):"},
            {"prompt": "Skiladagsetning (DD/MM/ÁÁÁÁ):"},
            {"prompt": "Skilatími (KK:MM):"},
        ]
        footer = "TIP: Veldu insláttarreit með enter til að hefja innslátt"
        menu = Menu(
            header=header, inputs=inputs, footer=footer,
            submit_function=self.submit_time_period, back_function=self.back,
            stop_function=self.stop,
        )
        return menu

    def __make_category_option_menu(self):
        from_date, to_date = self.__selected_date_range
        day_count = abs((from_date - to_date).days)
        header = "".join((
            self.__controller_header, " -> Leigutímabil -> Veldu bílaflokk\n",
            "Hér getur þú valið einn bílaflokk. Verðið er miðað af þessum",
            " flokk, og því er hægt að sjá það hér líka.\n"
            "\n{:<24}Verð á dag\t\tFullt verð ({} dagar)".format('', day_count)
        ))
        prices = self.__price_list_repo.get_all()
        categories = [price["category"] for price in prices]
        choose = self.go_to_pickup_branch_choice
        options = list()
        for price in prices:
            cat = "{:<12}\t".format(price["category"] + ":")
            category = ''.join((cat, str(price["price"]), " kr."))
            full_price = price["price"] * day_count
            category += "\t\t {} kr.".format(full_price)
            opt = {"description": category, "value": choose}
            options.append(opt)
        return Menu(header=header, options=options, back_function=self.back,
                    stop_function=self.stop,)

    def __make_branch_option_menu(self, to=False):
        header_list = [
            self.__controller_header, 
            " -> Leigutímabil -> Veldu bílaflokk",
            " -> Sótt í útibúi"
        ]
        if to:
            header_list.append(" -> Skilað í útibúi")
            header_list.append("\n Veldu útibú til að skila bílnum í")
            choice = self.go_to_search
        else:
            header_list.append("\nVeldu útibú til að sækja bílinn í")
            choice = self.go_to_return_branch_choice
        header = "".join(header_list)
        branches = BranchRepository().get_all()
        opts = [{"description": brnch, "value": choice} for brnch in branches]
        return Menu(header=header, options=opts, back_function=self.back,
                    stop_function=self.stop,)

    def __make_customer_select_menu(self):
        header = "".join((
            "Leigja bíl -> Innskráning",
            "\n\nHefur þú ekki leigt bíl áður hjá Bílaleigu Björgvins?",
            "\nÞú getur skráð þig með því að velja 'Skrá nýjann viðskiptavin'",
            "\n\nEf þú ert skráður í kerfið er nóg að slá inn ",
            "ökuskírteinisnúmerið þitt hér:"
        ))
        inputs = [{"prompt": "Ökuskírteinisnúmer:"}]
        options = [
            {"description": "Skrá inn", "value": self.log_in},
            {"description": "Skrá nýjann viðskiptavin", "value": self.register}
        ]
        result_menu = Menu(
            header=header, inputs=inputs, options=options, can_submit=False,
            back_function=self.back, stop_function=self.stop
        )
        return result_menu

    def __make_extra_insurance_menu(self):
        insurance_price = RentOrder.EXTRA_INSURANCE
        insurance = self.get_insurance
        no_insurance = self.skip_insurance
        header = "".join((
            self.__controller_header,
            " -> Leigutímabil -> Veldu bílaflokk",
            " -> Valin útibú -> Valinn bíll -> Tryggingar",
            "\n\nGrunntrygging er innifalin í öllum pöntunum, en",
            "hvað gerist ef þú klessir á í órétti?",
            "\nLausnin er að hugsa fyrirfram. Við bjóðum upp á",
            ' ódýra kaskó aukatryggingu á fyrir aðeins ', str(insurance_price),
            " kr og rétt að sálinni þinni við andlát.",
            "\n\nViltu aukatryggingu?",
        ))
        options = [
            {"description": "Já \t+" + str(insurance_price) + " kr.",
                "value": insurance},
            {"description": "Nei\t+0 kr.", "value": no_insurance},
        ]
        return Menu(header=header, options=options, back_function=self.back,
                    stop_function=self.stop,)

    def __make_order_report_menu(self, order):
        extra_insurance_price = order.get_total_cost() - order.get_base_cost()
        extra_insurance_price -= order.get_addon_price()
        car = order.get_car()
        addon_str = ", ".join(car.get_extra_properties())
        order_str = "".join((
            "Pöntun númer: ", str(order.get_order_number()),
            "\nUpphafstími leigu: ", str(order.get_pickup_time()),
            "\nÁætlaður skilatími: ", str(order.get_estimated_return_time()),
            "\nTegund bíls: ", car.get_name(),
            "\nNafn leigjanda: ", order.get_customer().get_name(),
            "\nAukahlutir á bíl: ", addon_str,
            "\n\nGrunnverð: ", str(order.get_base_cost()), " kr.",
            "\nAukatrygging: ", str(extra_insurance_price), " kr.",
            "\nVerð á aukahlutum: ", str(order.get_addon_price()), " kr."
            "\nHEILDARVERÐ: ", str(order.get_total_cost()), " kr.",
        ))
        header = "".join((
            self.__controller_header,
            " -> Leigutímabil -> Veldu bílaflokk  -> Valin útibú",
            " -> Valinn bíll -> Tryggingar -> Klára pöntun",
            "\n\nHérna er pöntunin þín:\n", order_str,
            "\n\n Þú getur valið hvort þú viljir borga fyrir pöntunina núna,",
            " eða þegar þú skilar bílnum."
        ))
        options = [
            {"description": "Borga núna", "value": self.pay_now},
            {"description": "Borga við lok leigu", "value": self.pay_later},
        ]
        return Menu(
            header=header, options=options, back_function=self.back,
            stop_function=self.stop,
        )

    def __make_order_success_menu(self):
        debt = self.__order.get_remaining_debt()
        header = "".join((
            "Leigja bíl -> Leigutímabil -> Veldu bílaflokk  -> Valin útibú ->",
            " Valinn bíll -> Tryggingar -> Klára pöntun -> Lokið\n\n"
            "Pöntunin þín er komin í kerfið. ",
            "Eftirstöður á reikningi eru ", str(debt), " krónur.",
            "\n\n\nGóða ferð frá BÍLALEIGU BJÖRGVINS!\n"
        ))
        return Menu(
            header=header, stop_function=self.stop, can_go_back=False
        )
