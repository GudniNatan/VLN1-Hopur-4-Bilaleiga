from controllers.controller_service import CarRentalService
from ui.splash_screen import splash_screen


def main():
    splash_screen()
    service = CarRentalService()
    service.start()


main()