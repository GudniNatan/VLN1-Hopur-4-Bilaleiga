from msvcrt import getwch
import os


class InputLine(object):
    def __init__(self, prompt="", default_text="", type_=""):
        self.__left_side = default_text
        self.__right_side = ""
        self.__cursor = "█"
        self.__active = False
        self.__prompt = prompt
        self.__is_password = str(type_).lower() == "password"

    def keypress(self, char, special=False):
        if not self.__active:
            return
        elif char == chr(10075):  # left arrow key
            self.move_cursor_left()
        elif char == chr(10077):  # right arrow key
            self.move_cursor_right()
        elif char == chr(10083):  # delete key
            self.__right_side = self.__right_side[1:]
        elif char == "\x08":
            self.__left_side = self.__left_side[0:-1]
        elif char not in ["�", "\r"]:
            self.__left_side += char

    def move_cursor_left(self):
        try:
            char = self.__left_side[-1]
            self.__left_side = self.__left_side[:-1]
            self.__right_side = char + self.__right_side
        except IndexError:  # there are no more characters on the left
            pass

    def move_cursor_right(self):
        try:
            char = self.__right_side[0]
            self.__right_side = self.__right_side[1:]
            self.__left_side += char
        except IndexError:  # there are no more characters on the right
            pass

    def set_active(self, boolean):
        self.__active = boolean

    def __str__(self):
        cursor = self.__cursor
        prompt = self.__prompt
        left_side = self.__left_side
        right_side = self.__right_side
        if prompt:
            prompt = prompt.strip() + " "
        if not self.__active:
            cursor = ""
        if self.__is_password:
            left_side = "*" * len(left_side)
            right_side = "*" * len(right_side)
        return "{}{}{}{}\n".format(prompt, left_side, cursor, right_side)

    def get_input(self):
        return (self.__left_side + self.__right_side).strip()


if __name__ == "__main__":
    inputLine = InputLine()
    os.system("cls")
    print(inputLine)
    while True:
        key = ord(getwch())
        if key == 224:
            key = ord(getwch())
            inputLine.keypress(key, True)
        else:
            if key == 13:
                break
            inputLine.keypress(chr(key))
        os.system("cls")
        print(inputLine)
    print(inputLine.get_input())
