from django.core.management.base import BaseCommand
from dataentry.models import  Student


class Command(BaseCommand):
    help = "Data Insert"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str, help="Help to data insertation")

    def handle(self, *args, **kwargs):
        name = kwargs["name"]
        greeting = f"Hi {name}! Good Luck"
        self.stdout.write(self.style.SUCCESS(greeting))
