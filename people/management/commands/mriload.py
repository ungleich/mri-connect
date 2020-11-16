from django.core.management.base import BaseCommand, CommandError
from people.loader.people import queue_refresh

class Command(BaseCommand):
    help = 'Imports from a ProClim database export'

    def add_arguments(self, parser):
        parser.add_argument('filename')
        parser.add_argument('--delim', nargs='?', default=',')
        parser.add_argument('--cols', nargs='?', default='Name,FirstName')

    def handle(self, *args, **options):
        fn = options['filename']
        delimiter = options['delim']
        required_cols = options['cols'].split(',')

        msg = queue_refresh(fn, required_cols, delimiter)
        if msg is not None: print(msg)

        self.stdout.write(self.style.SUCCESS('Successfully imported from %s' % fn))
