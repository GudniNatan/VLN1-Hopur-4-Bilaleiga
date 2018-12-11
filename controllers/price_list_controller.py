from controllers.controller import Controller
from ui.menu import Menu


class PriceListController(Controller):
    def __init__(self, service, priority_controller=False):
        super().__init__(service, priority_controller)
        self._menu_stack.append(self.__make_price_chart_menu())

    def __make_price_chart_menu(self):
        header = "temp"
        menu = Menu(header=header, stop_function=self.stop,
                    back_function=self.back)
        return menu
