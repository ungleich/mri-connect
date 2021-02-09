import shutil
from pathlib import Path

from django.contrib.auth.forms import PasswordResetForm
from django.core.management import BaseCommand

from expert_management.models import User


class Command(BaseCommand):
    help = "Broadcast Password Reset"

    def add_arguments(self, parser):
        parser.add_argument('file_path', help="Path to email template. A sample email template is provided at docs/email_template.html")

    def handle(self, *args, **options):
        file_path = Path(options["file_path"])

        template_directory = Path("expert_management/templates/email")
        template_directory.mkdir(exist_ok=True)

        email_template_name_path_in_project = template_directory / file_path.name
        email_template_name = Path(*email_template_name_path_in_project.parts[-2:])

        shutil.copyfile(file_path, email_template_name_path_in_project)

        for user in User.objects.filter(last_login__isnull=True):
            form = PasswordResetForm({'email': user.email})
            if form.is_valid():
                form.save(email_template_name=email_template_name)

        shutil.rmtree(template_directory, ignore_errors=True)
