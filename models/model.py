from abc import ABC, abstractmethod

# This is the model base class. It is mostly just an abstract
# class to define what a model class needs to have.


class Model(ABC):
    @abstractmethod
    def csv_repr(self) -> dict:
        return dict()

    @abstractmethod
    def get_dict(self) -> dict:
        return self.csv_repr()

    @abstractmethod
    def __eq__(self, other):
        pass

    @abstractmethod
    def get_key(self):  # Each model has a key
        return None

    @abstractmethod
    def get_name(self):  # Each model has a human-readable name
        return None
