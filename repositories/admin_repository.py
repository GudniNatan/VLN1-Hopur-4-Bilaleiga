from repositories.staff_repository import StaffRepository


class AdminRepository(StaffRepository):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)
