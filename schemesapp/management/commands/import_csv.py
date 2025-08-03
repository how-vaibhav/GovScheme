import csv
from django.core.management.base import BaseCommand
from schemesapp.models import Scheme

class Command(BaseCommand):
    help = 'Import data from CSV into MyModel'

    def handle(self, *args, **kwargs):
        with open('schemes_data/sikkim_schemes.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Scheme.objects.create(
                    name=row['Scheme Name'],
                    objective=row['Objective'],
                    benefits=row['Benefits'],
                    agency=row['Implementing Agency']
                )
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))