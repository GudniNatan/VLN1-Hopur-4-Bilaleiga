from controllers.controller import Controller
from ui.menu import Menu


class HelpMenuController(Controller):
    def __init__(self, service, priority_controller=False):
        super().__init__(service, priority_controller)
        self._menu_stack.append(self.__make_help_menu())

    def __make_help_menu(self):
        header = self.__create_help_header()
        menu = Menu(header=header, stop_function=self.stop,
                    back_function=self.back)
        return menu

    def __create_help_header(self):
        dashline = "-" * 120 + "\n"
        header = "".join((
            "Velkominn í bókunarkerfi Bílaleigu Björgvins. ",
            "Kerfið er ætlað starfsmönnum fyrirtækisins og ",
            "fólki sem vill bóka bíla \nrafrænt.\n",
            dashline,
            "Starfsmenn skulu skrá sig inná kerfið ",
            "áður en notkun á því hefst.\n",
            dashline,
            "Kerfið er ætlað til notkunar í CLI(Command line glugga) ",
            "og því virka ekki músasmellir á neitt.\n",
            "Allt er birt í textaformi og þeir valmöguleikar sem eru í ",
            "boði eru merktir með tölum.\n",
            "Hægt er að velja úr möguleikunum með því að færa örina „>” ",
            "upp og niður og smella á enter til að velja.\n",
            "Einnig er hægt að velja hluti beint með því að slá inn ",
            "viðeigandi tölustaf eða bókstaf.\n",
            "Þegar það er reitur sem þarf að skrifa í þá þarf fyrst að velja ",
            "hann áður en hægt er að skrifa síðan hægt að smella á \n",
            "enter til að fara í næsta reit eða til að klára ferlið á ",
            "skjánum (Þegar það á við)\n",
            dashline,
            "Styttingar:\n",
            "0: Eyðir (þegar það er í boði)\n",
            "B: Fer alltaf til baka um eitt skref\n",
            "Q: Hættir því sem er verið að gera og fer á forsíðu\n",
            "Esc: Fer úr innsláttarreit\n",
            dashline,
            "Allur réttur áskilinn af Glaumbæjargenginu, 2018\n",
            dashline
        ))
        return header.strip()
