from abc import ABC, abstractmethod
import os


class Menu(ABC):
    _header_message = ''
    _footer_message = ''

    @abstractmethod
    def getInput(self):
        return 0

    def display(self):
        print(self)

    def clearScreen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
