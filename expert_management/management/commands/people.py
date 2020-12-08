from django.core.management.base import BaseCommand, CommandError
from expert_management.models import Expert, Affiliation, Project, Topic, Expertise

class Command(BaseCommand):
    help = 'Manages the Experts database'

    actions = ['activate', 'delete']

    def add_arguments(self, parser):
        parser.add_argument('action', help='An action to run on the Experts database: %s' % ', '.join(self.actions))
        parser.add_argument('--emails', nargs='?', default='', help='A list of Expert addresses, separated by commas')
        parser.add_argument('--full', action='store_true', help='When deleting, include all related objects')

    def handle(self, *args, **options):
        action = options['action']

        if action == 'activate':
            if not 'emails' in options:
                print("--emails option required")
                return
            emails = options['emails'].split(',')
            c = 0
            for email in emails:
                if not '@' in email.strip(): continue
                try:
                    expert = Expert.objects.get(
                        contact_email = email.strip()
                    )
                    expert.allow_public = True
                    expert.save()
                    c += 1
                except Expert.DoesNotExist:
                    continue
            self.stdout.write(self.style.SUCCESS('Activated %d users' % c))

        elif action == 'delete':
            if not input("Confirm with Y deletion of all imported (ProClim) profiles? ").lower() == 'y':
                return
            query = Expert.objects.exclude(proclimid__isnull=True).exclude(proclimid__exact='')
            count = query.count()
            query.delete()
            self.stdout.write(self.style.SUCCESS('Deleted %d users' % count))
            if 'full' in options:
                Affiliation.objects.all().delete()
                Project.objects.all().delete()
                Expertise.objects.all().delete()
                Topic.objects.all().delete()
                self.stdout.write(self.style.SUCCESS('Deleted all related objects'))

        else:
            self.stdout.write(self.style.WARNING('Invalid action'))
