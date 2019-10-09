from abc import ABC, abstractmethod
import csv

# This is the repository base class.
# Repos can do a whole bunch of different things, but the only
# thing any inheriting repos need to implement is a function
# that translates a dictionary to its model object type.


class Repository(ABC):
    _FILENAME = ""
    _TYPE = None
    _PRIMARY_KEY = ""  # name of primary key
    _CSV_ROW_NAMES = list()

    def add(self, model_object: _TYPE):
        """Add the model object to the csv file."""
        for item in self.get_all():  # Update the repo if model already exists
            if item == model_object:
                self.update(model_object)
                return
        with open(self._FILENAME, "a+", newline='', encoding="utf8") as fl_ptr:
            csv_dict_writer = csv.DictWriter(
                fl_ptr, fieldnames=self._CSV_ROW_NAMES, delimiter=";"
            )
            representation = model_object.csv_repr()
            csv_dict_writer.writerow(representation)

    def write(self, model_object_list: list):
        """Write the csv file with the given object list."""
        with open(self._FILENAME, "w", newline='', encoding="utf8") as fl_ptr:
            csv_dict_writer = csv.DictWriter(
                fl_ptr, fieldnames=self._CSV_ROW_NAMES, delimiter=";"
            )
            reps = [model_obj.csv_repr() for model_obj in model_object_list]
            csv_dict_writer.writeheader()
            csv_dict_writer.writerows(reps)

    def update(self, model_object: _TYPE, key=None):
        """Update the csv files representation of model_object.

        Raises ValueError if the object to update is not found.
        """
        model_object_list = self.get_all()
        if key is None:
            index = model_object_list.index(model_object)
        else:
            for i, some_model_object in enumerate(model_object_list):
                if some_model_object.get_key() == key:
                    index = i
                    break
        model_object_list[index] = model_object
        self.write(model_object_list)

    def remove(self, model_object: _TYPE):
        """Remove the model_object from the csv file.

        Raises ValueError if the object to remove is not found.
        """
        model_object_list = self.get_all()
        model_object_list.remove(model_object)
        self.write(model_object_list)

    def get(self, key):
        """Return the object with the given key.

        Raises ValueError if an object with the given key is not found.
        """
        file = self.__read_file()
        for line in file:
            if str(line[self._PRIMARY_KEY]).lower() == str(key).lower():
                return self.dict_to_model_object(line)
        raise ValueError("Fann ekki {} í {}".format(
            key, self._FILENAME
        ))

    def get_all(self):
        file = self.__read_file()
        model_objects = list()
        for line in file:
            read_object = self.dict_to_model_object(line)
            model_objects.append(read_object)
        return model_objects

    def __read_file(self):
        file = list()
        with open(self._FILENAME, encoding="utf8") as file_pointer:
            csv_dict_reader = csv.DictReader(file_pointer, delimiter=";")
            file.extend(csv_dict_reader)
        return file

    def remove_by_key(self, key):
        """Remove line in the file where the primary key value is equal to key.

        Will raise ValueError if the object to remove is not found.
        """
        model_object = self.get(key)
        self.remove(model_object)
        pass

    def get_row_names(self):
        return self._CSV_ROW_NAMES

    @abstractmethod
    def dict_to_model_object(self, a_dict):
        """Translate a dict to this model."""
        return self._TYPE(**a_dict)
