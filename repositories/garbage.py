class Stuff():
    def __init__(self, name, id__, test):
        self.name = name
        self.id = id__
        self.test = test

    def __str__(self):
        return " ".join((self.name, str(self.id), self.test))


my_dict = {"name": "wow", "id__": 123, "test": "i am just testing"}

my_stuff = Stuff(**my_dict)

print(my_stuff)