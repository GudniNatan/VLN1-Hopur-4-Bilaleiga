from controllers.controller import Controller
from repositories.car_repository import CarRepository
from repositories.branch_repository import BranchRepository
from repositories.price_list_repository import PriceListRepository
from repositories.customer_repository import CustomerRepository
from controllers.manage_customers_controller import ManageCustomersController
from ui.menu import Menu
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

    def submit_time_period(self, values, menu):
        from_date = values[0:2]
        to_date = values[2:4]
        try:
            self._validation.validate_rent_range(from_date, to_date)
        except ValueError as error_msg:
            menu.set_errors((error_msg,))
            return
        self.__selected_date_range = (from_date, to_date)
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
            in_branch=self.__selected_pickup_branch
        )
        self._menu_stack.append(self._ui.get_search_result_menu(
            results, self.__controller_header, self.choose_car
        ))

    def choose_car(self, car, menu):
        self.__selected_car = car
        self._menu_stack.append(self.__make_customer_select_menu())

    def log_in(self, values, menu):
        driver_license_id = values[0]
        try:
            customer = self.__customer_repo.get(driver_license_id)
        except ValueError:
            error_msg = "".join((
                "Enginn viðskiptavinur með þetta ökuskírteinisnúmer ",
                "fannst. Ertu örugglega skráð/ur?"
            ))
            menu.set_errors((error_msg,))
            return
        self.__selected_customer = customer
        self._menu_stack.append(self.__make_customer_select_menu())

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
        header = "".join((
            self.__controller_header, " -> Leigutímabil -> Veldu bílaflokk"
        ))
        prices = self.__price_list_repo.get_all()
        categories = [price["category"] for price in prices]
        choose = self.go_to_pickup_branch_choice
        options = list()
        for price in prices:
            cat = "{:<12}".format(price["category"] + ":")
            category = ''.join((cat, str(price["price"]), " kr. á dag"))
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
