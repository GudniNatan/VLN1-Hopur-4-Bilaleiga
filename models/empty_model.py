class EmptyModel():
    def __init__(self, name):
        self.__name = name

    def csv_repr(self) -> dict:
        return dict()

    def get_dict(self) -> dict:
        return self.csv_repr()

    def __eq__(self, other):
        return False

    def get_key(self):  # Each model has a key
        return ""

    def get_name(self):  # Each model has a human-readable name
        return ""
