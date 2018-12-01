from services.CarRentalService import CarRentalService
from ui.Menu import Menu


class CarRentalUI(object):
    def __init__(self):
        self.car_rental_service = CarRentalService()
        self.user_id = ""
        self.user_type = 0

    def welcome_menu(self):
        header = "Welcome to Bílaleiga Björgvins!"
        footer = "----------------------------------\nMove the pointer using the arrow keys!"
        options = ["Help", "Price chart", "Book a car", "", "Staff login"]
        welcome_menu_obj = Menu(header=header, footer=footer, options=options)
        selection = ""
        while selection != "Q":
            selection, values = welcome_menu_obj.get_input()
            if selection == 0:
                selection = self.help_menu()
            if selection == 2:
                selection = self.rental_pickup_time_menu()
    
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
        while selection != "Q":
            pickup_datetime = None
            while pickup_datetime is None:
                selection, values = rent_time_menu.get_input()
                if selection == "Q":
                    return selection
                pickup_datetime = self.car_rental_service.validate_datetime(values)
            selection = self.rental_return_time_menu(pickup_datetime)
        return selection

    def rental_return_time_menu(self, pickup_datetime):
        return "Q"
