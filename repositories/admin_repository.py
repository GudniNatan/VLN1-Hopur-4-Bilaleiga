from repositories.staff_repository import StaffRepository
from models.admin import Admin


class AdminRepository(StaffRepository):
    _FILENAME = "./data/Admins.csv"
    _TYPE = Admin
