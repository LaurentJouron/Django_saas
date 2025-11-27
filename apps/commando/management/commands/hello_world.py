from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Affiche 'Hello, World!' dans la console."

    def handle(self, *args, **kwargs):
        self.stdout.write("Hello, World!")
