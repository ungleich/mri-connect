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


class Role(models.TextChoices):
    CoordinationOfficeStaff = "Coordination Office Staff", "Coordination Office Staff"
    CoPi = "Co-PI", "Co-PI"
    SLCMember = "SLC-Member", "SLC-Member"


class WorkingGroup(models.TextChoices):
    EducationForSustainableMountainDevelopment = "Education for Sustainable Mountain Development", "Education for Sustainable Mountain Development"
    ElevationDependentClimateChange = "Elevation Dependent Climate Change", "Elevation Dependent Climate Change"
    MountainGovernance = "Mountain Governance", "Mountain Governance"
    MountainObservatories = "Mountain Observatories","Mountain Observatories"
    MountainResilience = "Mountain Resilience", "Mountain Resilience"


class InvolvementInMRIActivity(models.TextChoices):
    AdaptationAtAltitude = "Adaptation at Altitude", "Adaptation at Altitude"
    GlobalAssessment = "Global Assessment", "Global Assessment"
    ConectateAPlus = "Conéctate-A+", "Conéctate-A+"
    ContributionToIPCC = "Contribution to IPCC AR6", "Contribution to IPCC AR6"
    GeoMountains = "GEO Mountains", "GEO Mountains"
    SythesisWorkshops = "Synthesis Workshops", "Synthesis Workshops"


class GeoMountainsRole(models.TextChoices):
    DataProvider = "Data Provider", "Data Provider"
    DataUser = "Data user", "Data user",
    LeadOrCoLead = "Lead or Co-Lead", "Lead or Co-Lead"
    ObservatoryContactPoint = "Observatory Contact Point", "Observatory Contact Point"
    StaffMemberToSecretariat = "Staff member of the Secretariat to the Flagship or Initiative", "Staff member of the Secretariat to the Flagship or Initiative"
    SteeringCommitteeMember = "Steering Committee (Board, Advisory Ctte, etc) Member)", "Steering Committee (Board, Advisory Ctte, etc) Member)"


EXPERTS_PREFERENCES = (
    (
        "join_ecr",
        _(
            "I would like to join the MRI Early Career Researchers (ECRs) fellows group (for enrolled students, practitioners, or scholars within 5 years of obtaining last degree)"
        ),
    ),
    (
        "contact_me",
        _(
            "I allow the MRI to contact me about my profile and link to it in its communications channels (website, social media, newsletter article)."
        ),
    ),
    (
        "expert_registry",
        _(
            "I would like to be added to an experts registry for the MRI to connect me with external requests for consultancies, expertise, policy inputs, speaking roles, or interviews."
        ),
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
