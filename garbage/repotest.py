import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from repositories.car_repository import CarRepository
from repositories.branch_repository import BranchRepository
from repositories.rent_order_repository import RentOrderRepository
from repositories.customer_repository import CustomerRepository
from models.car import Car
from models.branch import Branch
from models.customer import Customer
from models.rent_order import RentOrder
from services.validation import Validation

my_branch = Branch("BB Reykjavík", "Flugvallarvegur, Reykjavík")

BranchRepository().add(my_branch)

my_car = Car(
    license_plate_number="AJ-123", model="My car model",
    category="Small car", wheel_count=4, drivetrain="4x4",
    automatic_transmission=True, seat_count=4,
    extra_properties={"A/C", "Heated seats"}, kilometer_count=100,
    current_branch=my_branch,
)

CarRepository().add(my_car)

my_read_car = CarRepository().get(my_car.get_license_plate_number())
my_read_branch = BranchRepository().get(my_branch.get_name())

print(my_read_car.get_dict())
print(my_read_branch.get_dict())

my_customer = Validation().validate_customer(
    driver_license_id="55lstfbs", personal_id="201101-2190",
    first_name="Guðni", last_name="Gunnarsson", birthdate="2001-11-20",
    phone_number="555-6969", email="gu@temala.is",
    cc_holder_first_name="Guðni", cc_holder_last_name="Gunnarsson",
    ccn="5372 8320 1588 4476", cc_exp_date="12/20"
)

print(my_customer.get_dict())
CustomerRepository().write((my_customer,))

for customer in CustomerRepository().get_all():
    print(customer.get_dict())

my_order = RentOrder()