from abc import ABC, abstractmethod
import csv
import typing


class Repository(ABC):
    _FILENAME = ""
    _TYPE = None
    _PRIMARY_KEY = ""  # name of primary key
    _CSV_ROW_NAMES = list()

    def add(self, model_object: _TYPE):
        '''Adds the model object to the csv file'''
        with open(self._FILENAME, "a+", newline='') as file_pointer:
            csv_dict_writer = csv.DictWriter(file_pointer,
                                             fieldnames=self._CSV_ROW_NAMES)
            representation = model_object.csv_repr()
            csv_dict_writer.writerow(representation)

    def write(self, model_object_list: list):
        ''' Writes the csv file with the given object list'''
        with open(self._FILENAME, "w", newline='') as file_pointer:
            csv_dict_writer = csv.DictWriter(file_pointer,
                                             fieldnames=self._CSV_ROW_NAMES)
            reps = [model_obj.csv_repr() for model_obj in model_object_list]
            csv_dict_writer.writeheader()
            csv_dict_writer.writerows(reps)

    def update(self, model_object: _TYPE):
        '''Update the csv files representation of model_object. Raises
        ValueError if the object to update is not found.'''
        model_object_list = self.get_all()
        index = model_object_list.index(model_object)
        model_object_list[index] = model_object
        self.write(model_object_list)

    def remove(self, model_object: _TYPE):
        '''Remove the model_object from the csv file. Raises
        ValueError if the object to remove is not found.'''
        model_object_list = self.get_all()
        model_object_list.remove(model_object)
        self.write(model_object_list)

    def get(self, key):
        '''Return the object with the given key. Raises ValueError
        if an object with the given key is not found.'''
        file = self.read_file()
        for line in file:
            if line[self._PRIMARY_KEY] == key:
                return self.dict_to_model_object(line)
        raise ValueError

    def get_all(self):
        file = self.read_file()
        model_objects = list()
        for line in file:
            read_object = self.dict_to_model_object(line)
            model_objects.append(read_object)
        return model_objects

    def read_file(self):
        file = list()
        with open(self._FILENAME) as file_pointer:
            csv_dict_reader = csv.DictReader(file_pointer)
            file.extend(csv_dict_reader)
        return file

    def remove_by_key(self, key):
        '''Remove the line in the csv file where the primary key value is
        equal to key. Will raise ValueError if the object to remove is not
        found.'''
        model_object = self.get(key)
        self.remove(model_object)
        pass

    @abstractmethod
    def dict_to_model_object(self, a_dict):
        return self._TYPE(**a_dict)
