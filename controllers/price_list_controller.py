from controllers.controller import Controller
from ui.menu import Menu
from repositories.price_list_repository import PriceListRepository


class PriceListController(Controller):
    def __init__(self, service, priority_controller=False):
        super().__init__(service, priority_controller)
        self._menu_stack.append(self.__make_price_chart_menu())
        self.__price_list_repo = PriceListRepository()

    def __make_price_chart_menu(self):
        header = self.__create_price_chart_header()
        menu = Menu(header=header, stop_function=self.stop,
                    back_function=self.back)
        return menu

    def __create_price_chart_header(self):
        dashline = "-" * 120 + "\n"
        price_list = self.__format_price_list()
        header = "".join((
            "Verðlisti\n",
            dashline,
            "\t----------------------------\n",
            "\t| Bílaflokkur | Verð á dag |\n",
            " \t|-------------|------------|\n",
            price_list,
            "\t----------------------------\n",
            "\n *ATH Hver aukahlutur kostar 50 kr aukalega á dag."
        ))
        return header.strip()

    def __format_price_list(self):
        formatted_price_list = ""
        template = "\t| {:<11} | {:>7} kr |\n"
        price_list_dict = PriceListRepository().get_all()
        for line in price_list_dict:
            formatted_price_list += template.format(line["category"],
                                                    line["price"])
        return formatted_price_list
