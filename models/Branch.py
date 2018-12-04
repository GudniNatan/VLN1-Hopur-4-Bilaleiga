from models.model import Model
import typing


class Branch(Model):
    def __init__(self, branch_name: str, address: str, cars: list()):
        self.branch_name = branch_name

    def csv_repr(self):
        return dict()

    def get_dict(self):
        return dict()
