import faker

from django.db import transaction
from django.db.models import Model
from address_manager.models import Address


def add_to_model(model: Model, rows: list[dict]):
    # Create a list of dictionaries with the address data
    instances = [model(**data) for data in rows]
    # Save the instance to the database
    with transaction.atomic():
        model.objects.bulk_create(instances)

def generate_addresses(n: int = 100):
    # set locale to pt_BR
    faker.Faker.seed(0)
    fake = faker.Faker('pt_BR')
    # Generate a list of addresses
    addresses = []
    # Add the address to the list
    for _ in range(n):
        address = {
            "zip_code": fake.postcode(),
            "street": fake.street_name(),
            "number": fake.building_number(),
            "complement": fake.building_number(),
            "neighborhood": fake.neighborhood(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "country": fake.country(),
            "reference": fake.sentence(nb_words=6),
        }
        addresses.append(address)
    # Add the addresses to the Address model and create them in bulk
    add_to_model(Address, addresses)
