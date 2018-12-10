from repositories.repository import Repository
from models.branch import Branch


class BranchRepository(Repository):
    _FILENAME = "./data/Branches.csv"
    _TYPE = Branch
    _PRIMARY_KEY = "name"  # name of primary key
    _CSV_ROW_NAMES = ["name", "address"]

    def dict_to_model_object(self, branch_dict):
        return Branch(**branch_dict)
