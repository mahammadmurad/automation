from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Create a new user'
    
    def handle(self, *args, **kwargs) :
        self.stdout.write('Any words')