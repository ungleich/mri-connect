import logging
import re

import numpy as np
import pandas as pd
from django.core.management import BaseCommand
from django.db import IntegrityError
from django.conf import settings

from expert_management import models
from expert_management.utils.common import non_zero_keys
from expert_management.utils.importdata import *
from expert_management.utils.mailchimp import Mailchimp

from mailchimp_marketing.api_client import ApiClientError

logger = logging.getLogger(__name__)

email_pattern = r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
email_pattern = re.compile(email_pattern, re.M)

class Command(BaseCommand):
    help_text = "Import data from old-database dump (.xlsx)"

    def add_arguments(self, parser):
        parser.add_argument("xlsx_file_path")
        parser.add_argument("--skip-mailchimp-sync", action="store_true")

    def handle(self, *args, **options):
        sheet = pd.read_excel(options["xlsx_file_path"], engine="openpyxl", index_col=0)
        sheet = sheet.replace({np.nan: None})
        skip_mailchimp_sync = options["skip_mailchimp_sync"]

        if not skip_mailchimp_sync:
            mailchimp = Mailchimp()

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
            email = row["EMailAddress"] or row["EMailAddress2"]
            comment = row["Comment"]

            # If user provided no email in EMailAddress and EMailAddress2 field but there is something in comment field
            if not email and comment:
                match = email_pattern.search(comment)
                if match:
                    email = match.group(0)


            personal_url = row["URL_site"]

            _expertise = row["Expertise"]
            _speciality = row["SpecialityOfPerson"]

            _parsed_expertise = parse_expertise(_expertise)
            _parsed_specialties = parse_speciality(_speciality, first_name, last_name)
            _parsed_expertise_and_specialities = _parsed_expertise + _parsed_specialties

            classified_expertise = classify_expertise(_parsed_expertise_and_specialities)

            #FIXME: This looks very bad. Note to me to refactor it someday
            research_expertise = return_existing_objects(
                classified_expertise.pop("research_expertise"),
                models.ResearchExpertise,
                lambda exp: models.ResearchExpertise.objects.get(title=exp)
            )
            atmospheric_sciences = return_existing_objects(
                classified_expertise.pop("atmospheric_sciences"),
                models.AtmosphericSciences,
                lambda exp: models.AtmosphericSciences.objects.get(title=exp)
            )
            hydrospheric_sciences = return_existing_objects(
                classified_expertise.pop("hydrospheric_sciences"),
                models.HydrosphericSciences,
                lambda exp: models.HydrosphericSciences.objects.get(title=exp)
            )
            cryospheric_sciences = return_existing_objects(
                classified_expertise.pop("cryospheric_sciences"),
                models.CryosphericSciences,
                lambda exp: models.CryosphericSciences.objects.get(title=exp)
            )
            earth_sciences = return_existing_objects(
                classified_expertise.pop("earth_sciences"),
                models.EarthSciences,
                lambda exp: models.EarthSciences.objects.get(title=exp)
            )
            biological_sciences = return_existing_objects(
                classified_expertise.pop("biological_sciences"),
                models.BiologicalSciences,
                lambda exp: models.BiologicalSciences.objects.get(title=exp)
            )
            social_sciences_and_humanities = return_existing_objects(
                classified_expertise.pop("social_sciences_and_humanities"),
                models.SocialSciencesAndHumanities,
                lambda exp: models.SocialSciencesAndHumanities.objects.get(title=exp)
            )
            integrated_systems = return_existing_objects(
                classified_expertise.pop("integrated_systems"),
                models.IntegratedSystems,
                lambda exp: models.IntegratedSystems.objects.get(title=exp)
            )
            spatial_scale_of_expertise = return_existing_objects(
                classified_expertise.pop("spatial_scale_of_expertise"),
                models.SpatialScaleOfExpertise,
                lambda exp: models.SpatialScaleOfExpertise.objects.get(title=exp)
            )
            statistical_focus = return_existing_objects(
                classified_expertise.pop("statistical_focus"),
                models.StatisticalFocus,
                lambda exp: models.StatisticalFocus.objects.get(title=exp)
            )
            time_scales = return_existing_objects(
                classified_expertise.pop("time_scales"),
                models.TimeScales,
                lambda exp: models.TimeScales.objects.get(title=exp)
            )
            methods = return_existing_objects(
                classified_expertise.pop("methods"),
                models.Methods,
                lambda exp: models.Methods.objects.get(title=exp)
            )
            participation_in_assessments = return_existing_objects(
                classified_expertise.pop("participation_in_assessments"),
                models.ParticipationInAssessments,
                lambda exp: models.ParticipationInAssessments.objects.get(title=exp)
            )
            inputs_or_participation_to_un_conventions = return_existing_objects(
                classified_expertise.pop("inputs_or_participation_to_un_conventions"),
                models.InputsOrParticipationToUNConventions,
                lambda exp: models.InputsOrParticipationToUNConventions.objects.get(title=exp)
            )

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
                    user = models.User.objects.create_user(
                        username=username, email=email, password=models.User.objects.make_random_password(length=32)
                    )
                    if not skip_mailchimp_sync:
                        response = mailchimp.get_member(email, settings.MAILCHIMP_LIST_ID)

                        if response:  # User found, but he/she may be archived
                            user.is_subscribed_to_newsletter = response["status"] == "subscribed"

                    for key in actual_user_data:
                        setattr(user, key, actual_user_data[key])

                    if affiliation:
                        user.affiliations.add(affiliation)

                    #FIXME: This looks very bad. Note to me to refactor it someday
                    models.Expertise(**classified_expertise, user=user).save()

                    user.expertise.research_expertise.add(*research_expertise)
                    user.expertise.atmospheric_sciences.add(*atmospheric_sciences)
                    user.expertise.hydrospheric_sciences.add(*hydrospheric_sciences)
                    user.expertise.cryospheric_sciences.add(*cryospheric_sciences)
                    user.expertise.earth_sciences.add(*earth_sciences)
                    user.expertise.biological_sciences.add(*biological_sciences)
                    user.expertise.social_sciences_and_humanities.add(*social_sciences_and_humanities)
                    user.expertise.integrated_systems.add(*integrated_systems)
                    user.expertise.spatial_scale_of_expertise.add(*spatial_scale_of_expertise)
                    user.expertise.statistical_focus.add(*statistical_focus)
                    user.expertise.time_scales.add(*time_scales)
                    user.expertise.methods.add(*methods)
                    user.expertise.participation_in_assessments.add(*participation_in_assessments)
                    user.expertise.inputs_or_participation_to_un_conventions.add(
                        *inputs_or_participation_to_un_conventions
                    )
                    user.save()

                except IntegrityError:
                    logger.info("Skipping personID %s because email %s already exists", person_id, email)
            else:
                if not username:
                    logger.info("Skipping personID %s because we can't figured out the username", person_id)

                if not email:
                    logger.info("Skipping personID %s because he/she does not have any email", person_id)
