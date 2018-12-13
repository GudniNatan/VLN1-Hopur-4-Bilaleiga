from repositories.repository import Repository
from models.branch import Branch


class BranchRepository(Repository):
    _FILENAME = "./data/Branches.csv"
    _TYPE = Branch
    _PRIMARY_KEY = "Nafn"  # name of primary key
    _CSV_ROW_NAMES = ["Nafn", "Heimilsfang"]

    def dict_to_model_object(self, branch_dict):
        args_list = [value for value in branch_dict.values()]
        return Branch(*args_list)
