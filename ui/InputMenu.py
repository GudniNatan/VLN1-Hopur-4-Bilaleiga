from Menu import Menu
from msvcrt import getch
import os
import sys


class InputMenu(Menu):
    def __init__(self, prompt, header_message='', footer_message=''):
        self.prompt = prompt
        self._header_message = header_message
        self._footer_message = footer_message
        self.__input_line = ""
        self.cursor = 0
    
    def display(self):
        super().display()
        print(self.prompt, self.__input_line, '█')
        print(self._footer_message)
    
    def getInput(self):
        self.display()
        key = ord(getch())
        self.clearScreen()
        if key == 80:
            self.cursor += 1
            self.cursor %= len(self.option_list)
        elif key == 72:
            self.cursor -= 1
            self.cursor %= len(self.option_list)
        elif key == 13:
            return self.cursor
        elif key == 27:
            return -1
        

