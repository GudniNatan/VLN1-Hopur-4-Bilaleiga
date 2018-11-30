from abc import ABC, abstractmethod
import os


class Menu(ABC):
    _header_message = ''
    _footer_message = ''

    @abstractmethod
    def get_input(self):
        return 0

    def display(self):
        print(self)

    def clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
