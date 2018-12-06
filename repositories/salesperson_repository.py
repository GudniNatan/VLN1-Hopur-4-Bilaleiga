from repositories.staff_repository import StaffRepository
from models.salesperson import Salesperson


class SalespersonRepository(StaffRepository):
    _FILENAME = "./data/Salespeople.csv"
    _TYPE = Salesperson
