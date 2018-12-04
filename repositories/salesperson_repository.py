from repositories.staff_repository import StaffRepository


class SalespersonRepository(StaffRepository):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

    def dict_to_model_object(self, staff_dict):
        pass
