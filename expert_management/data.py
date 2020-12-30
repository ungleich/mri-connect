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

RESEARCH_EXPERTISE = zip_with_itself(
    (
        "Basic Research",
        "Applied Research",
        "Research Interface and Management",
        "Interdisciplinary Research",
        "Transdisciplinary Research",
    )
)

ATMOSPHERIC_SCIENCES_SUBCATEGORIES = zip_with_itself(
    ("Meteorology", "Climatology", "Atmospheric Physics / Chemistry", "Pollution")
)

HYDROSPHERIC_SCIENCES_SUBCATEGORIES = zip_with_itself(
    ("Fresh Water Systems", "Precipitation and Runoff", "Hydrogeology")
)

CRYOSPHERIC_SCIENCES_SUBCATEGORIES = zip_with_itself(("Glaciology", "Snow Sciences", "Permafrost and solifluction"))

EARTH_SCIENCES_SUBCATEGORIES = zip_with_itself(
    (
        "Soil Science/Pedology",
        "Geomorphology",
        "Geochemistry",
        "Geology",
        "Physical Geography",
        "Geophysics",
    )
)

BIOLOGICAL_SCIENCES_SUBCATEGORIES = zip_with_itself(
    (
        "Botany",
        "Zoology",
        "Ecology",
        "Terrestrial Ecosystems",
        "Aquatic Ecosystems",
        "Soil organisms",
        "Forestry",
        "Ecosystem functioning",
        "Ecosystem services",
        "Biodiversity",
    )
)

SOCIAL_SCIENCES_AND_HUMANITIES_SUBCATEGORIES = zip_with_itself(
    (
        "History, classical studies, archaeology, prehistory and early history",
        "Linguistics and literature, philosophy",
        "Art studies, musicology, theatre and film studies, architecture",
        "Ethnology, social and human geography",
        "Psychology",
        "Educational studies",
        "Sociology, social work",
        "Political sciences",
        "Media and communication studies",
        "Public health",
        "Economics",
        "Law",
    )
)

INTEGRATED_SYSTEMS_SUBCATEGORIES = zip_with_itself(
    (
        "Carbon Cycle",
        "Other Biogeochemical Cycles",
        "Hydrogeochemical Cycle",
        "Nutrient Cycle",
        "Social-ecological Systems",
    )
)

SPATIAL_SCALE_OF_EXPERTISE = zip_with_itself(
    (
        "Global / Hemispheric",
        "Continental",
        "Regional",
        "National / Cultural",
        "Local / Community",
    )
)

STATISTICAL_FOCUS = zip_with_itself(
    (
        "Extremes",
        "Mean Change / Trends",
        "Variability",
    )
)

TIME_SCALES = zip_with_itself(
    (
        "Seasonal / Annual",
        "Decadal / Centennial",
        "Millenial",
        "100 kyr",
        "Billenial (Mio yrs)",
    )
)

METHODS = zip_with_itself(
    (
        "Earth Observations",
        "Remote sensing",
        "Field observations",
        "Field Experiments",
        "Modeling",
        "Spatial analyses",
        "Policy Analysis",
        "Qualitative social science methods",
        "Integrative assessments",
        "Synthesis and meta-analyses",
    )
)

ASSESSMENT_TYPES = zip_with_itself(("IPCC", "IPBES", "UNDRR GAR"))

UN_CONVENTIONS_POLICY_PROCESSES = zip_with_itself(
    ("UN Agenda 2030 (SDGs) / UN HLPF", "UNFCCC", "CBD", "UNDRR Sedai", "UNCCD")
)
