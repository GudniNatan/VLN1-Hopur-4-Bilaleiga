from Menu import Menu
from msvcrt import getch
import os
import sys


class InputMenu(Menu):
    def __init__(self, prompt, header_message='', footer_message='', pre_input=''):
        self.prompt = prompt
        self._header_message = header_message
        self._footer_message = footer_message
        self.__input_line = pre_input
        self.cursor = 0

    def getInput(self):
        key = 0
        self.clearScreen()
        while key != 13:
            self.display()
            the_input = getch()
            key = ord(the_input)
            self.clearScreen()
            if key == 80:
                self.cursor += 1
                self.cursor %= 3
            elif key == 72:
                self.cursor -= 1
                self.cursor %= 3
            elif key == 27:
                return -1
            elif self.cursor == 0:
                self.updateInputLine(the_input)
        cursor = self.cursor
        self.cursor = -1
        return cursor, self.__input_line

    def updateInputLine(self, key):
        char = key.decode('utf-8', errors='replace')
        if char == "\x08":
            self.__input_line = self.__input_line[0:-1]
        elif char not in ["�", "\r"]:
            self.__input_line += char

    def __str__(self):
        the_string = "{}\n".format(self._header_message)
        textCursorBox = "█" if self.cursor == 0 else "" 
        promt_line = "{} {}{}\n".format(self.prompt, self.__input_line, textCursorBox)
        if self.cursor == -1:
            return the_string + promt_line
        back_line = "Back"
        quit_line = "Quit"
        line_list = [promt_line, back_line, quit_line]
        for i, line in enumerate(line_list):
            the_string += "->" if self.cursor == i else "  "
            the_string += line + '\n'
        the_string += self._footer_message
        return the_string

if __name__ == "__main__":
    prompt = "What is your name:"
    menu = InputMenu(prompt, "My menu", "Bílaleiga Björgvins ©")
    cursor, name = menu.getInput()
    if cursor == 0:
        print("Your name is", name)
    elif cursor == 1:
        print("Go back!")
    else:
        print("I QUIT")
    menu2 = InputMenu("What is your age", menu, "Bílaleiga Björgvins ©")
    cursor, name = menu2.getInput()
    input()
