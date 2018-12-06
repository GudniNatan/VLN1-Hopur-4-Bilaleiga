class MenuOption(object):
    def __init__(self, value, descriptor: str, hotkey=None):
        self.__value = value
        self.__descriptor = descriptor
        if hotkey is None:
            self.__hotkey = str(value)[0]
        else:
            self.__hotkey = hotkey

    def __str__(self):
        return "[{}] {}".format(self.__hotkey, self.__descriptor)

    def get_hotkey(self):
        return self.__hotkey

    def get_value(self):
        return self.__value
