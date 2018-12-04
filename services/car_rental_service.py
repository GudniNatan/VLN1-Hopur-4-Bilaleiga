from services.controller import Controller
from services.main_menu_controller import MainMenuController


class CarRentalservice(object):
    def __init__(self):
        self.__controller_stack = list()
        self.__user_type = 0

    def start(self):
        controller_stack = self.__controller_stack
        controller_stack.append(MainMenuController)
        self.run()

    def run(self):
        controller_stack = self.__controller_stack
        while controller_stack:
            # the top-of-stack controller rules all
            controller = controller_stack[-1]
            controller.main()

    def add(self, controller):
        if isinstance(controller, Controller):
            self.__controller_stack.append(controller)
        else:
            raise ValueError("{} should be a controller.".format(controller))

    def pop(self, index=-1):
        return self.__controller_stack.pop(index)

    def pop_to_limit(self):
        controller_stack = self.__controller_stack
        controller = controller_stack.pop()
        while controller.is_pop_limit() is False and controller_stack:
            controller = controller_stack.pop()
        return controller

    def get_user_type(self):
        return self.__user_type

    def set_user_type(self, user_type: int):
        self.__user_type = user_type
