from services.CarRentalService import CarRentalService
from ui.Menu import Menu

QUIT = Menu.QUIT
BACK = Menu.BACK
SUBMIT = Menu.SUBMIT


class CarRentalUI(object):
    def __init__(self):
        self.car_rental_service = CarRentalService()
        self.user_id = ""
        self.user_type = 0

    def welcome_menu(self):
        header = "Welcome to Bílaleiga Björgvins!"
        footer = "{}\n{}".format(
            "----------------------------------",
            "Move the pointer using the arrow keys!")
        options = ["Help", "Price chart", "Book a car", "", "Staff login"]
        welcome_menu_obj = Menu(header=header, footer=footer, options=options)
        selection = ""
        while selection != "Q":
            selection, values = welcome_menu_obj.get_input()
            if selection == 0:
                self.help_menu()
            if selection == 2:
                self.rental_pickup_time_menu()
    
    def help_menu(self):
        header = """Velkominn í bókunarkerfi Bílaleigu Björgvins. Kerfið er ætluð starfsmönnum fyrirtækisins og fólki sem vill bóka bíla 
rafrænt
------------------------------------------------------------------------------------------------------------------------
Þeir sem eru ekki starfsmenn, vinsamlegast veljið annan kostinn þar sem stendur viðskiptavinir
------------------------------------------------------------------------------------------------------------------------
Kerfið er ætlað til notkunar í CLI(Command line glugga) og því virka ekki músasmellir á neitt.
Allt er birt í textaformi og þeir valmöguleikar sem eru í boði eru merktir með tölum.
Hægt er að velja úr möguleikunum með því að færa örina „>” upp og niður og smella á enter til að velja. 
Einnig er hægt að velja hluti beint með því að slá inn viðeigandi tölustaf.
Þegar það er reitur sem þarf að skrifa í þá þarf fyrst að velja hann áður en hægt er að skrifa
------------------------------------------------------------------------------------------------------------------------
Styttingar:
0: Eyðir (þegar það er í boði)
B: Fer alltaf til baka um eitt skref
F: Hættir því sem er verið að gera og fer á forsíðu
Esc: Virkar eins og 9 og hættir því sem er verið að gera og sendir aftur á forsíðu
------------------------------------------------------------------------------------------------------------------------
Allur réttur áskilinn af Glaumbæjargengið 
------------------------------------------------------------------------------------------------------------------------"""
        help_menu_obj = Menu(header=header)
        selection, values = help_menu_obj.get_input()
        return selection

    def rental_pickup_time_menu(self):
        header = "Rent a car\n{}\nEnter pick up date & time:".format("-" * 30)
        date_input = {"prompt": "Enter date [YYYY-MM-DD]: ", "type": "date"}
        time_input = {"prompt": "Enter time [HH:MM]: ", "type": "time"}
        inputs = [date_input, time_input]
        rent_time_menu = Menu(inputs=inputs, header=header)
        callback = ""
        while callback != "Q":
            pickup_datetime = None
            while pickup_datetime is None:
                selection, values = rent_time_menu.get_input()
                if selection == "Q":
                    return selection
                elif selection == "B":
                    return
                pickup_datetime = self.car_rental_service.validate_datetime(
                    values)
            callback = self.rental_return_time_menu(pickup_datetime)
        return callback

    def rental_return_time_menu(self, pickup_datetime):
        header = "Rent a car\n{}{}\nEnter return date & time:".format(
            str(pickup_datetime), "-" * 30)
        date_input = {"prompt": "Enter return date [YYYY-MM-DD]: ", "type": "date"}
        time_input = {"prompt": "Enter return time [HH:MM]: ", "type": "time"}
        inputs = [date_input, time_input]
        rent_time_menu = Menu(inputs=inputs, header=header)
        callback = ""
        while callback != QUIT:
            return_datetime = None
            while return_datetime is None:
                selection, values = rent_time_menu.get_input()
                if selection == QUIT:
                    return selection
                elif selection == BACK:
                    return
                validate = self.car_rental_service.validate_return_datetime
                return_datetime = validate(pickup_datetime, values)
            callback = self.rental_car_category_menu(pickup_datetime,
                                                     return_datetime)
        return callback

    def rental_car_category_menu(self, pickup_datetime, return_datetime):
        header = "{}\n{} {}\n{} {}\n{}".format(
            "Rent a car", "Pickup time:", str(pickup_datetime), "Return time:",
            str(return_datetime), "-" * 30,)
        category_options = ["Small car", "Crossover",
                            "SUV", "Minivan", "Sport"]
        category_menu = Menu(header=header, options=category_options)
        callback = ""
        while callback != QUIT:
            selection, values = category_menu.get_input()
            if selection == QUIT:
                return selection
            elif selection == BACK:
                return
            callback = self.choose_car_menu(
                pickup_datetime, return_datetime, selection)
        return callback

    def choose_car_menu(self, pickup_datetime, return_datetime, car_type):
        return "Q"
