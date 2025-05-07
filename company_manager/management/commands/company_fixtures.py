import faker
import random

from address_manager.models import Address
from company_manager.models import Company
from django.core.management.base import BaseCommand # Import BaseCommand
from django.db import transaction
from django.db.models import Model


# Helper function to add row dict to the model
def add_to_model(model: Model, rows: list[dict]):
    # Create a list of dictionaries with the address data
    instances = [model(**data) for data in rows]
    # Save the instance to the database
    with transaction.atomic():
        model.objects.bulk_create(instances)

def generate_companies(n: int = 100):
    # set locale to pt_BR
    fake = faker.Faker('pt_BR')
    # Generate a list of addresses
    companies = []
    # Add the address to the list
    for _ in range(n):
        random_pk = random.randint(1, 100),
        company = {
            "short_name": fake.company(),
            "name": fake.name(),
            "cnpj": fake.cnpj(),
            # random address foreign key
            "address": Address.objects.get(pk=100),
            "email": fake.email(),
            "phone": fake.phone_number(),
            "website": fake.url(),
            "description": fake.text(max_nb_chars=5),
        }
        companies.append(company)
    add_to_model(Company, companies)

# Define the Command class
class Command(BaseCommand):
    help = 'Generates fake companies and adds them to the database.'
    def handle(self, *args, **options):
        self.stdout.write("Generating fake companies...")
        try:
            generate_companies(10)
        except Exception as e:
            self.stdout.write(self.style.ERROR("Error generating companies."))
            # error message
            self.stdout.write(self.style.ERROR(f"Error: {e}"))
            return
        self.stdout.write(
            self.style.SUCCESS("Successfully generated and added companies.")
        )
