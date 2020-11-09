from django.core.management.base import BaseCommand, CommandError
from people.loader.people import queue_refresh

class Command(BaseCommand):
    help = 'Imports from a ProClim database export'

    def add_arguments(self, parser):
        parser.add_argument('filename')
        # parser.add_argument('delim')
        # parser.add_argument('cols')

    def handle(self, *args, **options):
        fn = options['filename']
        if 'delim' in options:
            delimiter = options['delim']
        else:
            delimiter = ","
        if 'cols' in options:
            required_cols = options['cols'].split(',')
        else:
            required_cols = ["Name", "FirstName"]
            
        msg = queue_refresh(fn, required_cols, delimiter)
        if msg is not None: print(msg)

        self.stdout.write(self.style.SUCCESS('Successfully imported from %s' % fn))
