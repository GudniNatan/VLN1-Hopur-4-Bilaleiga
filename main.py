from repositories.CarRepository import CarRepository
from models.Car import Car

def main():
    print("__________ __ __          __          __                    ")
    print("\______   \__|  | _____  |  |   ____ |__| _________         ")
    print(" |    |  _/  |  | \__  \ |  | _/ __ \|  |/ ___\__  \        ")
    print(" |    |   \  |  |__/ __ \|  |_\  ___/|  / /_/  > __ \_      ")
    print(" |______  /__|____(____  /____/\___  >__\___  (____  /      ")
    print("        \/             \/          \/  /_____/     \/       ")
    print("__________     __  _   _                    __               ")
    print("\______   \   |__||_|_|_|_____  _______  _|__| ____   ______")
    print(" |    |  _/   |  |/  _ \_  __ \/ ___\  \/ /  |/    \ /  ___/")
    print(" |    |   \   |  (  <_> )  | \/ /_/  >   /|  |   |  \\\___ \ ")
    print(" |______  /\__|  |\____/|__|  \___  / \_/ |__|___|  /____  >")
    print("        \/\______|           /_____/              \/     \/ ")

main()

a = CarRepository()
print(a.get_all())
for car in a.get_all():
    print(vars(car))
b = Car("BT-T54", "Honda Odyssey 2014", 4, True)
print(b.csv_repr())
a.add(b)
