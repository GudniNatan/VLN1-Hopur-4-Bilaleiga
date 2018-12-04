from repositories.repository import Repository


class StaffRepository(Repository):
    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)
