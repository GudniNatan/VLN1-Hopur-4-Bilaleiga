from abc import ABC, abstractmethod


class Model(ABC):
    @abstractmethod
    def csv_repr(self):
        return list()

    @abstractmethod
    def __eq__(self, other):
        pass
