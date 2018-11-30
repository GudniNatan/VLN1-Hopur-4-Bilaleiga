from Menu import Menu
from InputLine import InputLine
from msvcrt import getch
import os
import sys


class InputMenu(Menu):
    def __init__(self, prompts=list(), header_message='', footer_message='', pre_input=list()):
        self.prompts = prompts
        self._header_message = header_message
        self._footer_message = footer_message
        self.__input_lines = [pre_input[i] if i < len(pre_input) else "" for i in range(len(promts))]
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
            else:
                self.updateInputLine(the_input, self.cursor)
        return self.cursor, self.__input_line

    def updateInputLine(self, key, line_number):
        char = key.decode('utf-8', errors='replace')
        try:
            if char == "\x08":
                self.__input_lines[line_number] = self.__input_lines[line_number][0:-1]
            elif char == "\r":
                self.__input_lines[line_number] += "\n"
            elif char != "�":
                self.__input_lines[line_number] += char
        except IndexError:
            pass

    def __str__(self):
        the_string = "{}\n".format(self._header_message)
        promt_line = "{} {}█\n".format(self.prompt, self.__input_line)
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
    input()
