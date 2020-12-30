import logging

import numpy as np
import pandas as pd
from django.core.management import BaseCommand
from django.db import IntegrityError

from expert_management.models import Affiliation, Expertise, User
from expert_management.utils.common import non_zero_keys
from expert_management.utils.importdata import *

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help_text = "Import data from old-database dump (.xlsx)"

    def add_arguments(self, parser):
        parser.add_argument("xlsx_file_path")

    def handle(self, *args, **options):
        sheet = pd.read_excel(options["xlsx_file_path"], engine="openpyxl", index_col=0)
        sheet = sheet.replace({np.nan: None})

        for person_id, row in sheet.iterrows():
            last_name = row["Name"]
            first_name = row["FirstName"]
            title = row["Title"]
            gender = parse_gender(row["Sex"])
            position = row["PPosition"]

            affiliation_abbreviation = row["UnivCompAbbr"]
            affiliation_fullname = row["UnivCompName"]
            affiliation_country = row["CountryName"]
            affiliation_street = row["Street"]
            affiliation_zip = row["ZIPCode"]
            affiliation_city = row["City"]

            affiliation = create_or_get_affiliation(
                affiliation_abbreviation, affiliation_fullname, affiliation_street,
                affiliation_city, affiliation_zip, affiliation_country
            )

            email = row["EMailAddress"] if row["EMailAddress"] else row["EMailAddress2"]

            personal_url = row["URL_site"]

            _expertise = row["Expertise"]
            _speciality = row["SpecialityOfPerson"]

            _parsed_expertise = parse_expertise(_expertise)
            _parsed_specialties = parse_speciality(_speciality, first_name, last_name)
            _parsed_expertise_and_specialities = _parsed_expertise + _parsed_specialties

            classified_expertise = classify_expertise(_parsed_expertise_and_specialities)

            username = get_unique_username(first_name, last_name)
            if username and email:
                actual_user_data = non_zero_keys(
                    {
                        "first_name": first_name,
                        "last_name": last_name,
                        "title": title,
                        "gender": gender,
                        "position": position,
                        "url_personal": personal_url,
                    }
                )
                try:
                    user = User.objects.create_user(username=username, email=email)

                    for key in actual_user_data:
                        setattr(user, key, actual_user_data[key])

                    if affiliation:
                        user.affiliations.add(affiliation)

                    user.save()
                    Expertise(**classified_expertise, user=user).save()
                except IntegrityError:
                    logger.info("Skipping personID %s because email %s already exists", person_id, email)
            else:
                if not username:
                    logger.info("Skipping personID %s because we can't figured out the username", person_id)

                if not email:
                    logger.info("Skipping personID %s because he/she does not have any email", person_id)
