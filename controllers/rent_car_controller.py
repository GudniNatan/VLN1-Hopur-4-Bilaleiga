from controllers.controller import Controller
from repositories.car_repository import CarRepository
from repositories.price_list_repository import PriceListRepository
from ui.menu import Menu
from services.search import Search


class RentCarController(Controller):
    def __init__(self, service, shortcut_to_register=False,
                 priority_controller=False):
        super().__init__(service, priority_controller)
        self.__controller_header = "Leigja bíl"
        self.__car_repo = CarRepository()
        self.__price_list_repo = PriceListRepository()
        self._menu_stack.append(self.__make_main_menu())
        self.__selected_date_range = None

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

    def __make_main_menu(self):
        header = " ".join((
            self.__controller_header,
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
        prices = self.__price_list_repo.get_all()
        categories = [price["category"] for price in prices]
        options = {"description": category for}