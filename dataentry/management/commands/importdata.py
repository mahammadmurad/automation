from django.core.management.base import BaseCommand, CommandError
from dataentry.utils import check_csv_errors
# from dataentry.models import Student
import csv
from django.apps import apps
from django.db import DataError


class Command(BaseCommand):
    help = "Import Data From CSV File"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Path to CSV file")
        parser.add_argument("model_name", type=str, help="Name of the model to import")

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        model_name = kwargs["model_name"].capitalize()
        
        model = check_csv_errors(file_path, model_name)

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)

            for row in reader:
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS("Data successfully imported"))
