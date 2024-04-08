import csv
from django.core.management.base import BaseCommand, CommandParser
from dataentry.models import *
from django.apps import apps
from dataentry.utils import generate_csv_file

# this command export data from any models
class Command(BaseCommand):
    help = "Export data from database to CSV format"

    def add_arguments(self, parser):
        parser.add_argument("model_name", type=str, help="Name of the model")

    def handle(self, *args, **kwargs):
        model_name = kwargs["model_name"].capitalize()
        model = None

        for app_config in apps.get_app_configs():
            try:
                model = apps.get_model(app_config.label, model_name)
                break
            except LookupError:
                pass

        if not model:
            self.stderr.write(f"Model {model_name} not found")
            return

        datas = model.objects.all()
        file_path = generate_csv_file(model_name)


        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            # for header in csv file
            writer.writerow([field.name for field in model._meta.fields])

            # for writing data to file
            for data in datas:
                writer.writerow(
                    [getattr(data, field.name) for field in model._meta.fields]
                )
        self.stdout.write(self.style.SUCCESS("Data exported successfully"))


# this command export data from specified models
# class Command(BaseCommand):
#     help = "Export data from model to CSV format"

#     def handle(self, *args, **kwargs):
#         students = Student.objects.all()

#         timestamp = datetime.datetime.now().strftime("%Y-%m-%d")

#         file_path = f"exported_data_{timestamp}.csv"

#         with open(file_path, "w", newline="") as file:
#             writer = csv.writer(file)
#             # for header in csv file
#             writer.writerow(["Roll No", "Name", "Age"])

#             # for writing data to file
#             for student in students:
#                 writer.writerow([student.roll_no, student.name, student.age])
#         self.stdout.write(self.style.SUCCESS("Data exported successfully"))
