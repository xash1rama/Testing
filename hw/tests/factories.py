import factory
import random
from faker import Faker
from python_advanced.module_29_testing.hw.main.app import db
from python_advanced.module_29_testing.hw.main.models import Client, ClientParking, Parking

card = factory.Faker('credit_card_number')
facer = Faker()
class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    credit_card =random.choice([None, random.randint(1000,9999)])
    car_number = factory.LazyFunction(facer.license_plate)


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker('city')
    opened = random.choice([True, False])
    count_places = random.randint(100,300)
    count_available_places = count_places

# class ClientParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
#     class Meta:
#         model = ClientParking
#         sqlalchemy_session = db.session
#
#     client_id = factory.Faker('city')
#     parking_id = factory.LazyAttribute(lambda x: random.choice([True, False]))
#     time_in:datetime
#     time_out:datetime
