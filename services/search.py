from repositories.car_repository import CarRepository


def search_cars(self, licence_plate_number, category, is_automatic,
                hide_available, hide_unavailable):
    if is_automatic:
        is_auto_first_letter = is_automatic[0].upper()
        if is_auto_first_letter == "J" or is_auto_first_letter == "Y":
            is_automatic = True
        else:
            is_automatic = False
    cars = CarRepository().get_all()
    for i in range(len(cars)-1, -1, -1):
        car = cars[i]
        if is_automatic:
            is_auto_first_letter = is_automatic[0].upper()
            if is_auto_first_letter in ["J", "Y"]:
                if not car.get_automatic_transmission():
                    cars.pop(i)
                    continue
            if is_auto_first_letter == "N":
                if car.get_automatic_transmission():
                    cars.pop(i)
                    continue
        if licence_plate_number not in ["", car.get_licence_plate_number()]:
            cars.pop(i)
        elif category and category != car.get_category():
            cars.pop(i)
        elif hide_available[0].upper() in ["J", "Y"]:
            pass
        elif hide_unavailable[0].upper() in ["J", "Y"]:
            pass
