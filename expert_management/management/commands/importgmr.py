import pandas as pd
import numpy as np

from django.core.management import BaseCommand
from django.db import IntegrityError

from expert_management.models import GeoMountainsRegistry, User
from expert_management.data import GeoMountainsRole
from expert_management.utils.importdata import get_unique_username


MAPPING_TABLE = {
    "Lead or Co-lead": GeoMountainsRole.LeadOrCoLead,
    "Staff member of the Secretariat to the Flagship or Initiative": GeoMountainsRole.StaffMemberToSecretariat,
    "Steering Committee (Board, Advisory Ctte, etc) Member": GeoMountainsRole.SteeringCommitteeMember,
}


class Command(BaseCommand):
    help_text = "Import Geo Mountain Registry Excel Sheet"

    def add_arguments(self, parser):
        parser.add_argument("sheet_path", help="Path to Geo Mountain Registry Excel Sheet")

    def handle(self, *args, **options):
        sheet_path = options["sheet_path"]

        sheet = pd.read_excel(sheet_path, engine="openpyxl", index_col=0, skiprows=1).replace({np.nan: None})

        for first_name, row in sheet.iterrows():
            last_name = row['Last Name'].strip()
            email = row['Email Address']
            primary_role = str.strip(row['Primary Role'] or '')
            primary_role = MAPPING_TABLE.get(primary_role, None)
            if primary_role:
                primary_role = [primary_role]
            user = User.objects.filter(first_name=first_name, last_name=last_name)

            # NOTE: If no user found with first_name and last_name, we try with the email
            # not trying with the email first is because some people have changed their
            # email. But, this approach of find user with names can be inaccurate as someother
            # person can have the same name as the actual member of Geo Mountain Registry

            if not user:
                user = user.union(User.objects.filter(email=email))
            user = user.first()

            if not user:
                # We need to create the user
                username = get_unique_username(first_name, last_name)
                user = User.objects.create_user(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    password=User.objects.make_random_password(length=32)
                )
            try:
                GeoMountainsRegistry.objects.get_or_create(user=user, role=primary_role)
            except IntegrityError:
                # Some entries are duplicated in the excel sheet, so we just skip them
                pass
