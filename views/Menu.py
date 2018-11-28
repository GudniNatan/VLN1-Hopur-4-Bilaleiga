from msvcrt import getch
import os
import sys
from abc import ABC, abstractmethod


class Menu(ABC):
    @abstractmethod
    def display(self):
        pass

    @abstractmethod
    def getSelection(self):
        return 0


class SelectMenu(Menu):
    def __init__(self, option_list, header_message='', footer_message=''):
        self.option_list = option_list
        self.cursor = 0
        self.header_message = header_message
        self.footer_message = footer_message

    def display(self):
        print(self.header_message)
        for i, option in enumerate(self.option_list):
            print("->" if i == self.cursor else "  ", end="")
            print("[" + str(i) + "]", end=" ")
            print(option)
        print(self.footer_message)

    def choose(self, item_key=None):
        if item_key is None:
            item_key = list(self.optionActionDict.keys())[self.cursor]
        return self.optionActionDict[item_key]()

    def menu(self):
        out = " "
        while out:
            print(out)
            self.display()
            key = ord(getch())
            os.system('cls')
            if key == 80:
                self.cursor += 1
                self.cursor %= len(self.optionActionDict)
            elif key == 72:
                self.cursor -= 1
                self.cursor %= len(self.optionActionDict)
            elif key == 13:
                out = self.choose()
            elif key == 27:
                break