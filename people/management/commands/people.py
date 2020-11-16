from django.core.management.base import BaseCommand, CommandError
from people.models import Person

class Command(BaseCommand):
    help = 'Manages the Persons database'

    def add_arguments(self, parser):
        parser.add_argument('action', help='An action to run on the Persons database: activate')
        parser.add_argument('--emails', nargs='?', default='', help='A list of Person addresses, separated by commas')

    def handle(self, *args, **options):
        action = options['action']
        emails = options['emails'].split(',')

        if action == 'activate':
            c = 0
            for email in emails:
                if not '@' in email.strip(): continue
                try:
                    person = Person.objects.get(
                        contact_email = email.strip()
                    )
                    person.allow_public = True
                    person.save()
                    print(person)
                    c += 1
                except Person.DoesNotExist:
                    continue
            self.stdout.write(self.style.SUCCESS('Activated %d users' % c))
        else:
            self.stdout.write(self.style.WARNING('Invalid action'))
