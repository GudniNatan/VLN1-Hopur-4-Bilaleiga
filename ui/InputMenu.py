from Menu import Menu
from InputLine import InputLine
from msvcrt import getwch, kbhit
import os
import sys


class InputMenu(Menu):
    def __init__(self, prompt, header_message='', footer_message='', pre_input='', back_message='Back', quit_message='Quit'):
        self.prompt = prompt
        self._header_message = header_message
        self._footer_message = footer_message
        self.__input_line = InputLine(prompt, pre_input)
        self.back_message = back_message
        self.quit_message = quit_message
        self.cursor = 0

    def get_input(self):
        key = 0
        self.clear_screen()
        while key != 13:
            self.display()
            key = ord(getwch())
            self.clear_screen()
            self.__process_input(key)
        cursor = self.cursor
        self.cursor = -1
        return cursor, self.__input_line

    def __process_input(self, key, ):
        if key == 224:
            key = ord(getwch())
            if key == 80:
                self.cursor += 1
                self.cursor %= 3
            elif key == 72:
                self.cursor -= 1
                self.cursor %= 3
            elif key == 27:
                return -1
            else:
                self.__input_line.keypress(key, True)
        elif self.cursor == 0:
            self.__input_line.keypress(chr(key))

    def __str__(self):
        the_string = "{}\n".format(self._header_message)
        self.__input_line.setActive(self.cursor == 0)
        if self.cursor == -1:
            return the_string + str(self.__input_line)
        back_line = "Back"
        quit_line = "Quit"
        line_list = [str(self.__input_line), back_line, quit_line]
        for i, line in enumerate(line_list):
            the_string += "->" if self.cursor == i else "  "
            the_string += line + '\n'
        the_string += self._footer_message
        return the_string

if __name__ == "__main__":
    prompt = "What is your name:"
    menu = InputMenu(prompt, "My menu", "Bílaleiga Björgvins ©")
    cursor, name = menu.get_input()
    if cursor == 0:
        print("Your name is", name)
    elif cursor == 1:
        print("Go back!")
    else:
        print("I QUIT")
    menu = InputMenu("What is your age: ", menu, "Bílaleiga Björgvins ©")
    cursor, name = menu.get_input()
    input()
