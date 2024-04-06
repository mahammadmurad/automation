from django.core.management.base import BaseCommand, CommandError

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

        model = None
        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                continue

        if not model:
            raise CommandError(f"Model {model_name} not found")

        model_fields = [field.name for field in model._meta.fields if field.name != 'id']

        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            csv_header = reader.fieldnames

            if csv_header != model_fields:
                raise DataError(
                    f"Model {model_name} does not match the field {csv_header}"
                )

            for row in reader:
                model.objects.create(**row)
        self.stdout.write(self.style.SUCCESS("Data successfully imported"))
