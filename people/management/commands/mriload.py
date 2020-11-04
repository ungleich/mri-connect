from django.core.management.base import BaseCommand, CommandError
from people.loader.people import load_people

class Command(BaseCommand):
    help = 'Imports from a ProClim database export'

    def add_arguments(self, parser):
        parser.add_argument('filename')

    def handle(self, *args, **options):
        fn = options['filename']
        load_people(fn)
        self.stdout.write(self.style.SUCCESS('Successfully imported from %s' % fn))
