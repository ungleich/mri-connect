from django.contrib.gis.db import models
from django.utils.translation import ugettext_lazy as _


class Title(models.TextChoices):
    MR = 'MR', 'Mr.'
    MS = 'MS', 'Ms.'
    MRS = 'MRS', 'Mrs.'
    DR = 'DR', 'Dr.'
    PROF = 'PROF', 'Prof.'
    PROF_EMERITUS = 'PROF_EMERIT', 'Prof. emerit.'


class Gender(models.TextChoices):
    MALE = 'M', _('Male')
    OTHER = 'F', _('Female')
    FEMALE = 'O', _('Other')


class CareerStage(models.TextChoices):
    UNDERGRAD = 'UNDERGRAD', _("Undergraduate student (e.g. BSc/BA)")
    POSTGRAD = 'POSTGRAD', _("Postgraduate student (Masters/PhD student)")
    POSTDOC = 'POSTDOC', _("Postdoc/Junior Researcher")
    ACADEMIC = 'ACADEMIC', _("Academic (Senior Researcher, Professor)")
    PUBLICSECTOR = 'PUBLICSECTOR', _("Practitioner in the public/government sector")
    PRIVATESECTOR = 'PRIVATESECTOR', _("Practitioner or business in the private sector")
    OTHER = 'OTHER', _("Other (short text)")


EXPERTS_PREFERENCES = (
    ('join_ecr', _("Would you like to join the MRI Early Career Researchers (ECRs) fellows group? (applies to currently enrolled students, practitioners, or postgraduate/postdoctoral scholars up to 5 years since obtaining last degree)")),
    ('contact_me', _("I allow MRI to contact me regarding my profile, as listed on the database, to link to and promote in its communications channels (website, social media, newsletter article).")),
    ('expert_registry', _("I would like to be added to an experts registry for internal use by the MRI Coordination Office to identify and connect with external requests for consultancies, expertise, provide inputs for policy briefs/policy reviews, speaking role, or interviews (such as by third parties, journalists or collaborators of the MRI).")),
    ('newsletter', _("I would like to receive monthly MRI Global Newsletters and Newsflashes from the MRI")),
)

AUTH_SPECIFIC_FIELDS = ("username", "password", "groups", "user_permissions", "date_added", "date_edited", "date_joined", "last_login", "is_staff", "is_superuser", "is_active", "email")

RESEARCH_EXPERTISE = (
    ('basic_research', 'Basic Research'),
    ('applied_research', 'Applied Research'),
    ('research_interface_and_management', 'Research Interface and Management'),
    ('interdisciplinary_research', 'Interdisciplinary Research'),
    ('transdisciplinary_research', 'Transdisciplinary Research'),
)

ATMOSPHERIC_SCIENCES_SUBCATEGORIES = (
    ("meteorology", "Meteorology"),
    ("climatology", "Climatology"),
    ("atmospheric_physics_or_chemistry", "Atmospheric Physics/Chemistry"),
    ("pollution", "Pollution")
)

HYDROSPHERIC_SCIENCES_SUBCATEGORIES = (
    ("fresh_water_systems", "Fresh Water Systems"),
    ("precipitation_and_runoff", "Precipitation and Runoff"),
    ("hydrogeology", "Hydrogeology")
)

CRYOSPHERIC_SCIENCES_SUBCATEGORIES = (
    ("glaciology", "Glaciology"),
    ("snow_sciences", "Snow Sciences"),
    ("permafrost_and_solifluction", "Permafrost and solifluction")
)

EARTH_SCIENCES_SUBCATEGORIES = (
    ("soil_science_or_pedology", "Soil Science/Pedology"),
    ("geomorphology", "Geomorphology"),
    ("geochemistry", "Geochemistry"),
    ("geology", "Geology"),
    ("physical_geography", "Physical Geography"),
    ("geophysics", "Geophysics")
)

BIOLOGICAL_SCIENCES_SUBCATEGORIES = (
    ("botany", "Botany"),
    ("zoology", "Zoology"),
    ("ecology", "Ecology"),
    ("terrestrial_ecosystems", "Terrestrial Ecosystems"),
    ("aquatic_ecosystems", "Aquatic Ecosystems"),
    ("soil_organisms", "Soil organisms"),
    ("forestry", "Forestry"),
    ("ecosystem_functioning", "Ecosystem functioning"),
    ("ecosystem_services", "Ecosystem services"),
    ("biodiversity", "Biodiversity"),
)

SOCIAL_SCIENCES_AND_HUMANITIES_SUBCATEGORIES = (
    ("history-classical_studies-archaeology-prehistory_and_early_history", "History, classical studies, archaeology, prehistory and early history"),
    ("linguistics_and_literature-philosophy", "Linguistics and literature, philosophy"),
    ("art_studies-musicology-theatre_and_film_studies-architecture", "Art studies, musicology, theatre and film studies, architecture"),
    ("ethnology-social_and_human_geography", "Ethnology, social and human geography"),
    ("psychology", "Psychology"),
    ("educational_studies", "Educational studies"),
    ("sociology-social_work", "Sociology, social work"),
    ("political_sciences", "Political sciences"),
    ("media_and_communication_studies", "Media and communication studies"),
    ("public_health", "Public health"),
    ("economics", "Economics"),
    ("law", "Law"),
)

INTEGRATED_SYSTEMS_SUBCATEGORIES = (
    ("carbon_cycle", "Carbon Cycle"),
    ("other_biogeochemical_cycles", "Other Biogeochemical Cycles"),
    ("hydrogeochemical_cycle", "Hydrogeochemical Cycle"),
    ("nutrient_cycle", "Nutrient Cycle"),
    ("social_ecological_systems", "Social-ecological Systems")
)

SPATIAL_SCALE_OF_EXPERTISE = (
    ("global_or_hemispheric", "Global / Hemispheric"),
    ("continental", "Continental"),
    ("regional", "Regional"),
    ("national_or_cultural", "National / Cultural"),
    ("local_or_community", "Local / Community"),
)

STATISTICAL_FOCUS = (
    ("extremes", "Extremes"),
    ("mean_change_or_trends", "Mean Change / Trends"),
    ("variability", "Variability"),
)

TIME_SCALES = (
    ("seasonal_or_annual", "Seasonal / Annual"),
    ("decadal_or_centennial", "Decadal / Centennial"),
    ("millenial", "Millenial"),
    ("100_kyr", "100 kyr"),
    ("billenial", "Billenial (Mio yrs)")
)

METHODS = (
    ("earth_observations", "Earth Observations"),
    ("remote_sensing", "Remote sensing"),
    ("field_observations", "Field observations"),
    ("field_experiments", "Field Experiments"),
    ("modeling", "Modeling"),
    ("spatial_analyses", "Spatial analyses"),
    ("policy_analysis", "Policy Analysis"),
    ("qualitative_social_science_methods", "Qualitative social science methods"),
    ("integrative_assessments", "Integrative assessments"),
    ("synthesis_and_meta-analyses", "Synthesis and meta-analyses"),
)

ASSESSMENT_TYPES = (
    ("ipcc", "IPCC"),
    ("ipbes", "IPBES"),
    ("undrr_gar", "UNDRR GAR")
)

UN_CONVENTIONS_POLICY_PROCESSES = (
    ("un_agenda_2030_or_un_hlpf", "UN Agenda 2030 (SDGs) / UN HLPF"),
    ("unfccc", "UNFCCC"),
    ("cbd", "CBD"),
    ("undrr_sedai", "UNDRR Sedai"),
    ("unccd", "UNCCD")
)
