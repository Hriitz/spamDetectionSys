import random
from faker import Faker
from django.core.management.base import BaseCommand
from api.models import PersonalContact

fake = Faker()

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of sample data to generate')

    def handle(self, *args, **options):
        count = options['count']

        for _ in range(count):
            name = fake.name()
            phone_number = fake.phone_number()
            email = fake.email() if random.choice([True, False]) else None

            PersonalContact.objects.create(
                name=name,
                phone_number=phone_number,
                email=email,
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully populated the database with {count} sample data'))
