from Menu import Menu
from msvcrt import getch
import os
import sys


class SelectMenu(Menu):
    def __init__(self, option_list, header_message='', footer_message=''):
        self.option_list = option_list
        self.cursor = 0
        self._header_message = header_message
        self._footer_message = footer_message

    def display(self):
        super().display()
        for i, option in enumerate(self.option_list):
            print("->" if i == self.cursor else "  ", end="")
            print("[" + str(i) + "]", end=" ")
            print(option)
        print(self._footer_message)

    def getInput(self):
        key = 0
        while key != 13:
            self.display()
            key = ord(getch())
            self.clearScreen()
            if key == 80:
                self.cursor += 1
                self.cursor %= len(self.option_list)
            elif key == 72:
                self.cursor -= 1
                self.cursor %= len(self.option_list)
            elif key == 27:
                return -1
        return self.cursor


if __name__ == "__main__":
    my_list = ["option 1", "selection II", "choice three", "val D"]
    menu = SelectMenu(my_list, "My menu")
    a = menu.getInput()
    print(a)