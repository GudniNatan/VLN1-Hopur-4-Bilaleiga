from ui.InputLine import InputLine
from msvcrt import getwch
import os
import sys


class Menu(object):
    __CURSOR = "->"
    QUIT = "Q"
    BACK = "B"
    SUBMIT = "S"

    def __init__(self, header="", errors=list(), inputs=list(), options=list(),
                 footer="", cursor_position=0, page=0, max_options_per_page=7):
        self.__header = header
        self.__errors = errors
        self.__options = options
        self.__footer = footer
        self.__cursor_position = cursor_position
        self.__page_number = page
        self.__max_options_per_page = max_options_per_page
        self.__page_count = len(self.__options) // self.__max_options_per_page
        self.__input_lines = list()
        for input_info in inputs:
            prompt = input_info.get("prompt", "")
            default = input_info.get("default", "")
            type_ = input_info.get("type", "text")
            input_line = InputLine(prompt, default, type_)
            self.__input_lines.append(input_line)
        self.__display_lines = self.__get_display_lines()
        self.__selected_input = None
        if self.__display_lines[cursor_position] in ["", "\n"]:
            self.move_cursor(1)
        self.__select_input_by_cursor()

    def display(self):
        display_string = "{}\n\n".format(self.__header)
        if self.__errors:
            display_string += "ERROR(S):\n"
        for error in self.__errors:
            display_string += "{}\n".format(error)

        for i, line in enumerate(self.__display_lines):
            if line:
                cursor = " " * len(self.__CURSOR)
                if self.__cursor_position == i:
                    cursor = self.__CURSOR
                display_string += cursor + str(line)
        display_string += "\n{}".format(self.__footer)
        self.clear_screen()
        print(display_string.strip())

    def __get_display_lines(self):
        display_lines = list()
        option_lines = self.__get_options_page_strings()
        nav_lines = self.__get_nav_strings()
        if self.__input_lines:
            display_lines.extend(self.__input_lines + ["\n"])
        display_lines.extend(option_lines)
        display_lines.extend(nav_lines)
        return display_lines

    def __get_page_start_end(self):
        page_start = self.__page_number * self.__max_options_per_page
        page_end = page_start + self.__max_options_per_page
        page_end = min(page_end, len(self.__options))
        return page_start, page_end

    def __get_options_page_strings(self):
        page_option_strings = list()
        page_start, page_end = self.__get_page_start_end()
        for i in range(page_start, page_end):
            option_string = "[{}] {}\n".format(i + 1, self.__options[i])
            if not self.__options[i]:
                option_string = "\n"
            page_option_strings.append(option_string)
        if page_option_strings:
            page_option_strings[-1] += "\n"
        return page_option_strings

    def __get_nav_strings(self):
        page_start, page_end = self.__get_page_start_end()
        last_page_string = ""
        next_page_string = ""
        submit_string = ""
        if len(self.__input_lines) > 0:
            submit_string = "Submit\n"
        if page_start > 0:
            last_page_string = "Previous page: ({}/{})\n".format(
                self.__page_number, self.__page_count)
        if page_end < len(self.__options):
            next_page_string = "Next page: ({}/{})\n".format(
                self.__page_number+2, self.__page_count)
        back_string = "[{}] Back\n".format(self.BACK)
        quit_string = "[ESC] Quit to main menu\n".format(self.QUIT)

        return [submit_string, last_page_string, next_page_string,
                back_string, quit_string]

    def get_input(self):
        menu_completed = False
        while not menu_completed:
            self.display()
            key = ord(getwch())
            menu_completed = self.__process_input(key)
            if menu_completed in [self.QUIT, self.BACK, self.SUBMIT]:
                return menu_completed, self.__input_lines
        cursor = self.__cursor_position
        if cursor == len(self.__display_lines) - 1:
            cursor = "Q"
        elif cursor == len(self.__display_lines) - 2:
            cursor = self.BACK
        elif cursor == len(self.__display_lines) - 5:
            cursor = self.SUBMIT
        else:
            if self.__input_lines:
                cursor -= len(self.__input_lines) + 1
            cursor = cursor + self.__page_number * self.__page_count
        return cursor, [input_line.get_input() for input_line
                        in self.__input_lines] 

    def __process_input(self, key, ):
        if key == 224:  # special char
            key = ord(getwch())
            if key == 80:  # arrow down
                self.move_cursor(1)
            elif key == 72:  # arrow up
                self.move_cursor(-1)
            elif self.__selected_input is not None:
                self.__selected_input.keypress(key, True)
        elif key == 27:  # esc
            if self.__selected_input is None:
                return self.QUIT
            else:
                self.move_cursor()
        elif key == 9:
            self.move_cursor(1)
            self.__select_input_by_cursor()
        elif key == 13:  # return
            # if cursor is by a input check if its selected
            # if the input is selected move cursor down and select the next
            # input if there is an input there
            # if the input is not selected, select it
            # if the cursor is not by an input, submit the selection.
            # unless the cursor by page controls, then flip the page.
            selected_input = self.__display_lines[self.__cursor_position]
            if type(selected_input) == InputLine:
                if selected_input == self.__selected_input:
                    self.move_cursor(1)
                self.__select_input_by_cursor()
            else:
                return True
        elif self.__selected_input is not None:
            self.__selected_input.keypress(chr(key))
        return False

    def move_cursor(self, distance=0):
        direction = distance >= 0    # True if down, False if up
        distance = abs(distance)
        cursor = self.__cursor_position
        while distance != 0:
            cursor += 1 if direction else -1
            cursor %= len(self.__display_lines)
            if self.__display_lines[cursor] not in ["", "\n"]:
                distance -= 1
        self.__cursor_position = cursor
        if self.__selected_input is not None:
            self.__selected_input.set_active(False)
            self.__selected_input = None

    def __change_page(self, page_number):
        if 0 <= page_number <= page_count:
            self.__page_number = page_number
        self.__display_lines = self.__get_display_lines()
        self.__cursor_position = 0
        self.move_cursor(-3)

    def __select_input_by_cursor(self):
        input_line = self.__display_lines[self.__cursor_position]
        if type(input_line) == InputLine:
            self.__selected_input = input_line
            self.__selected_input.set_active(True)

    def __str__(self):
        inputs = [str(line) for line in self.__input_lines]
        return "".join(inputs).strip()

    def clear_screen(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def set_errors(self, errors: list):
        self.__errors = errors


if __name__ == "__main__":
    my_inputs = [{"prompt": "Input name:"}, {"prompt": "Input age:"}]
    my_options = ["wow", "i", "am", "so", "algebraic"]
    menu = InputMenu(header="My menu", inputs=my_inputs, options=my_options,
                     footer="Bílaleiga Björgvins ©")
    cursor, name = menu.get_input()
    print(cursor)
    if cursor == "S":
        print("Your name is", name)
    elif cursor == "B":
        print("Go back!")
    elif cursor == "Q":
        print("I QUIT")
    menu = InputMenu((cursor, name), list(), [{"prompt": "Is this program awsome or what:", "default": "yes it is"}])
    cursor, name = menu.get_input()
    many_options = ["option #{}".format(i) for i in range(30)]
    menu = InputMenu(header="My pagified menu", options=many_options)
    print(menu.get_input())
    input()
