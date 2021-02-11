import shutil
from pathlib import Path

import bleach
from django.contrib.auth.forms import PasswordResetForm
from django.core.management import BaseCommand

from expert_management.models import User


def remove_link(attrs, new=False):
    link = attrs[(None, 'href')]
    if link:
        if link.startswith("mailto:"):
            link = f"email at {link[7:]}"

        attrs["_text"] = link
        attrs.pop((None, 'href'))
        return attrs
    return None

html_to_plain_text = lambda html: bleach.clean(
    bleach.linkify(html, callbacks=[remove_link]), tags=set(bleach.sanitizer.ALLOWED_TAGS) - {'a', 'i', 'b'}, strip=True
)


class Command(BaseCommand):
    help = "Broadcast Password Reset"

    def add_arguments(self, parser):
        parser.add_argument(
            'file_path',
            help="Path to email template. A sample email template is provided at docs/email_template.html"
        )
        parser.add_argument(
            '--subject',
            help="Subject of email"
        )
        parser.add_argument(
            '--email',
            help="Use this option, if you want to send reset-email to only a single person",
        )

    def handle(self, *args, **options):
        file_path = Path(options["file_path"])
        subject = options["subject"]
        email = options["email"]

        template_directory = Path("expert_management/templates/email")
        template_directory.mkdir(exist_ok=True)

        if not subject:
            subject_template_name = "registration/password_reset_subject.txt"
        else:
            subject_template_path = template_directory / "password_reset_subject.txt"
            subject_template_path.write_text(subject)
            subject_template_name = Path(*subject_template_path.parts[-2:])

        email_template_path_in_project = template_directory / file_path.name
        plain_text_email_template_path_in_project = template_directory / file_path.with_name(f"plain_{file_path.name}").name

        email_template_name = Path(*email_template_path_in_project.parts[-2:])
        plain_text_email_template_name = Path(*plain_text_email_template_path_in_project.parts[-2:])

        shutil.copyfile(file_path, email_template_path_in_project)

        email_template = html_to_plain_text(file_path.read_text())
        plain_text_email_template_path_in_project.write_text(email_template)

        extra_parms = {
            "use_https": True,
            "subject_template_name": subject_template_name
        }
        if file_path.suffix == ".html":
            extra_parms['html_email_template_name'] = email_template_name
            extra_parms['email_template_name'] = plain_text_email_template_name
        else:
             extra_parms['email_template_name'] = email_template_name

        recepients = User.objects.filter(email=email) if email else User.objects.filter(last_login__isnull=True)
        for user in recepients:
            form = PasswordResetForm({'email': user.email})
            if form.is_valid():
                form.save(**extra_parms)

        shutil.rmtree(template_directory, ignore_errors=True)
