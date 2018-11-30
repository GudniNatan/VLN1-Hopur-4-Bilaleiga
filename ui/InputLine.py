from msvcrt import getwch
import os


class InputLine(object):
    def __init__(self, prompt="", default_text=""):
        self.left_side = default_text
        self.right_side = ""
        self.cursor = "█"
        self.__active = True
        self.prompt = prompt

    def keypress(self, char, special=False):
        if not self.__active:
            return
        if special:
            if char == 75:  # left arrow key
                self.move_cursor_left()
            elif char == 77:  # right arrow key
                self.move_cursor_right()
            elif char == 83:
                self.right_side = self.right_side[1:]
        else:
            if char == "\x08":
                self.left_side = self.left_side[0:-1]
            elif char not in ["�", "\r"]:
                self.left_side += char

    def move_cursor_left(self):
        try:
            char = self.left_side[-1]
            self.left_side = self.left_side[:-1]
            self.right_side = char + self.right_side
        except IndexError:  # there are no more characters on the left
            pass

    def move_cursor_right(self):
        try:
            char = self.right_side[0]
            self.right_side = self.right_side[1:]
            self.left_side += char
        except IndexError:  # there are no more characters on the right
            pass

    def set_active(self, boolean):
        self.__active = boolean

    def __str__(self):
        if self.__active:
            return "{} {}{}{}\n".format(self.prompt, self.left_side,
                                        self.cursor, self.right_side)
        else:
            return "{} {}{}\n".format(self.prompt, self.left_side,
                                      self.right_side)


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
            inputLine.keypress(chr(key))
        os.system("cls")        
        print(inputLine)