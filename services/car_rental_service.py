from services.main_menu_controller import MainMenuController
from services.controller import Controller


class CarRentalService(object):
    def __init__(self):
        self.__controller_stack = list()
        self.__current_user = None

    def start(self):
        controller_stack = self.__controller_stack
        main_menu_controller = MainMenuController(self)
        controller_stack.append(main_menu_controller)
        self.run()

    def run(self):
        controller_stack = self.__controller_stack
        while controller_stack:
            # the top-of-stack controller rules all
            controller = controller_stack[-1]
            controller.main()

    def add(self, controller):
        if isinstance(controller, Controller):
            if self.__controller_stack:
                top_controller = self.__controller_stack[-1]
                top_controller.deactivate()
            self.__controller_stack.append(controller)
        else:
            raise ValueError("{} should be a controller.".format(controller))

    def pop(self, index=-1):
        return self.__controller_stack.pop(index)

    def pop_to_limit(self):
        controller_stack = self.__controller_stack
        self.pop()
        if not self.__controller_stack:
            return
        controller = controller_stack[-1]
        while controller.get_pop_limit() is False and controller_stack:
            controller = controller_stack.pop()
        return controller

    def get_current_user(self):
        return self.__current_user

    def set_current_user(self, user):
        self.__current_user = user
