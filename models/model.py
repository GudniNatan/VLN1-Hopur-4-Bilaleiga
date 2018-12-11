from abc import ABC, abstractmethod


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
    def get_key(self):
        return None
