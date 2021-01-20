from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _

from .utils.common import zip_with_itself


class Title(models.TextChoices):
    MR = "MR", "Mr."
    MS = "MS", "Ms."
    MRS = "MRS", "Mrs."
    DR = "DR", "Dr."
    PROF = "PROF", "Prof."
    PROF_EMERITUS = "PROF_EMERIT", "Prof. emerit."


class Gender(models.TextChoices):
    MALE = "M", _("Male")
    FEMALE = "F", _("Female")
    OTHER = "O", _("Other")


class CareerStage(models.TextChoices):
    UNDERGRAD = "UNDERGRAD", _("Undergraduate student (e.g. BSc/BA)")
    POSTGRAD = "POSTGRAD", _("Postgraduate student (Masters/PhD student)")
    POSTDOC = "POSTDOC", _("Postdoc/Junior Researcher")
    ACADEMIC = "ACADEMIC", _("Academic (Senior Researcher, Professor)")
    PUBLICSECTOR = "PUBLICSECTOR", _("Practitioner in the public/government sector")
    PRIVATESECTOR = "PRIVATESECTOR", _("Practitioner or business in the private sector")
    OTHER = "OTHER", _("Other (short text)")


EXPERTS_PREFERENCES = (
    (
        "join_ecr",
        _(
            "Would you like to join the MRI Early Career Researchers (ECRs) fellows group? (applies to currently enrolled students, practitioners, or postgraduate/postdoctoral scholars up to 5 years since obtaining last degree)"
        ),
    ),
    (
        "contact_me",
        _(
            "I allow MRI to contact me regarding my profile, as listed on the database, to link to and promote in its communications channels (website, social media, newsletter article)."
        ),
    ),
    (
        "expert_registry",
        _(
            "I would like to be added to an experts registry for internal use by the MRI Coordination Office to identify and connect with external requests for consultancies, expertise, provide inputs for policy briefs/policy reviews, speaking role, or interviews (such as by third parties, journalists or collaborators of the MRI)."
        ),
    ),
    (
        "newsletter",
        _("I would like to receive monthly MRI Global Newsletters and Newsflashes from the MRI"),
    ),
)

AUTH_SPECIFIC_FIELDS = (
    "username",
    "password",
    "groups",
    "user_permissions",
    "date_added",
    "date_edited",
    "date_joined",
    "last_login",
    "is_staff",
    "is_superuser",
    "is_active",
)
