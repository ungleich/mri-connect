# from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import m2m_changed
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField
from multiselectfield import MultiSelectField


def join_true_values(iterable, string=", "):
    return string.join(filter(lambda s: s, map(lambda x: "" if x is None else x, iterable)))

class Affiliation(models.Model):
    name = models.CharField(max_length=256, null=False, blank=False)
    department = models.CharField(max_length=256, null=True, blank=True)
    street = models.CharField(max_length=256, null=True, blank=True)
    post_code = models.CharField(max_length=256, null=True, blank=True)
    city = models.CharField(max_length=256, null=True, blank=True)
    country = CountryField(null=False, blank=False)

    @property
    def location(self):
        if not self.city: return self.country.name or ""
        if not self.country: return self.city or ""
        return ", ".join([
            self.city.strip(),
            self.country.name
        ])

    def __str__(self):
        return self.name
    class Meta:
        unique_together = [['name', 'department']]

class Project(models.Model):
    name = models.CharField(max_length=256)
    acronym = models.CharField(max_length=16, null=True, blank=True)
    date_start = models.DateField(null=True, blank=True)
    date_ending = models.DateField(null=True, blank=True)
    funding_source = models.CharField(max_length=256, null=True, blank=True)
    role = models.CharField(max_length=256, null=True, blank=True)
    homepage = models.URLField(null=True, blank=True, max_length=1024)
    location = models.CharField(max_length=256, null=True, blank=True, help_text="This is the location where the research is conducted or the fieldwork, not the home of research group/affiliation")
    coordinates = models.PointField()
    country = CountryField(null=True, blank=True, help_text="This is the country where the research is conducted or the fieldwork, not the home of research group/affiliation")

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.name

class Expertise(models.Model):
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

    research_expertise = MultiSelectField(choices=RESEARCH_EXPERTISE, null=True, blank=True)

    atmospheric_sciences = MultiSelectField(choices=ATMOSPHERIC_SCIENCES_SUBCATEGORIES, null=True, blank=True)
    hydrospheric_sciences = MultiSelectField(choices=HYDROSPHERIC_SCIENCES_SUBCATEGORIES, null=True, blank=True)
    cryospheric_sciences = MultiSelectField(choices=CRYOSPHERIC_SCIENCES_SUBCATEGORIES, null=True, blank=True)
    earth_sciences = MultiSelectField(choices=EARTH_SCIENCES_SUBCATEGORIES, null=True, blank=True)
    biological_sciences = MultiSelectField(choices=BIOLOGICAL_SCIENCES_SUBCATEGORIES, null=True, blank=True)
    social_sciences_and_humanities = MultiSelectField(choices=SOCIAL_SCIENCES_AND_HUMANITIES_SUBCATEGORIES, null=True, blank=True)
    integrated_sciences_and_humanities = MultiSelectField(choices=INTEGRATED_SYSTEMS_SUBCATEGORIES, null=True, blank=True)
    other_expertise = models.CharField(max_length=1024, null=True, blank=True, help_text="This should be a comma seperated list")

    spatial_scale_of_expertise = MultiSelectField(choices=SPATIAL_SCALE_OF_EXPERTISE, null=True, blank=True)
    other_spatial_scale_of_expertise = models.CharField(max_length=1024, null=True, blank=True, help_text="This should be a comma seperated list")

    statistical_focus = MultiSelectField(choices=STATISTICAL_FOCUS, null=True, blank=True)
    other_statistical_focus = models.CharField(max_length=1024, null=True, blank=True, help_text="This should be a comma seperated list")

    time_scales = MultiSelectField(choices=TIME_SCALES,null=True, blank=True)
    other_time_scales = models.CharField(max_length=1024, null=True, blank=True, help_text="This should be a comma seperated list")

    methods = MultiSelectField(choices=METHODS, null=True, blank=True)
    other_methods = models.CharField(max_length=1024, null=True, blank=True, help_text="This should be a comma seperated list")

    participation_in_assessments = MultiSelectField(choices=ASSESSMENT_TYPES, null=True, blank=True)
    other_participation_in_assessments = models.CharField(max_length=1024, null=True, blank=True, help_text="This should be a comma seperated list")
    more_detail_about_participation_in_assessments = models.TextField(null=True, blank=True)

    inputs_or_participation_to_un_conventions = MultiSelectField(choices=UN_CONVENTIONS_POLICY_PROCESSES, null=True, blank=True)
    other_inputs_or_participation_to_un_conventions = models.CharField(max_length=1024, null=True, blank=True, help_text="This should be a comma seperated list")

    # mountain_ranges_of_research_interest
    """
    Multiple choice (List of mountain ranges from GMBA mountain inventory:
    https://www.gmba.unibe.ch/services/tools/mountain_inventory;
    https://ilias.unibe.ch/goto_ilias3_unibe_cat_1000515.html)
    + text field for more specific location
    """
    # mountain_ranges_of_research_expertise (same as above)

    expert = models.OneToOneField("Expert", help_text="Research expertise", on_delete=models.CASCADE, related_name="expertise")

    @property
    def spatial_scale_expertise(self):
        return join_true_values([
            self.get_spatial_scale_of_expertise_display(), self.other_spatial_scale_of_expertise
        ])

    @property
    def statistical_focus_expertise(self):
        return join_true_values([
            self.get_statistical_focus_display(), self.other_statistical_focus
        ])

    @property
    def time_scale_expertise(self):
        return join_true_values([
            self.get_time_scales_display(), self.other_time_scales
        ])

    @property
    def methods_expertise(self):
        return join_true_values([
            self.get_methods_display(), self.other_methods
        ])

    @property
    def participation_in_assessments_details(self):
        return join_true_values([
            self.get_participation_in_assessments_display(),
            self.other_participation_in_assessments
        ])

    @property
    def inputs_or_participation_to_un_conventions_details(self):
        return join_true_values([
            self.get_inputs_or_participation_to_un_conventions_display(),
            self.other_inputs_or_participation_to_un_conventions
        ])
    class Meta:
        verbose_name = _('Expertise')
        verbose_name_plural = _('Expertise')


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


class ExpertManager(models.Manager):
    def get_by_natural_key(self, first_name, last_name):
        return self.get(first_name=first_name, last_name=last_name)

class Expert(models.Model):
    user = models.OneToOneField(get_user_model(), related_name="expert_profile", on_delete=models.CASCADE)

    date_added = models.DateField(auto_now_add=True)
    date_edited = models.DateField(auto_now=True)

    # 1-4
    last_name = models.CharField(max_length=128, null=False, blank=False)
    first_name = models.CharField(max_length=128, null=False, blank=False)
    title = models.CharField(max_length=16, null=True, blank=True, choices=Title.choices)
    gender = models.CharField(max_length=16, null=True, blank=True,
                              choices=Gender.choices)

    # 5
    position = models.CharField(max_length=256, null=False, blank=False)

    # 6
    affiliations = models.ManyToManyField(Affiliation, related_name="experts", blank=True, help_text="Upto 3 affiliations can be added.")

    # 7 Preferred email contact*
    contact_email = models.EmailField(null=False, blank=False, unique=True)

    # 8 I am..
    career_stage = models.CharField(max_length=16,
                                    null=True, blank=True,
                                    choices=CareerStage.choices, verbose_name="I am ")
    # 8
    career_stage_note = models.CharField(_("Other"),
                                    null=True, blank=True,
                                    max_length=256)

    # 9
    year_of_last_degree_graduation = models.PositiveIntegerField(
        _("Year of last degree graduation"),
        null=True, blank=True,
        validators=[
            MinValueValidator(1900), MaxValueValidator(2100)
        ])

    # 9.1
    preferences = MultiSelectField(
        choices=EXPERTS_PREFERENCES, null=True, blank=True
    )

    # 10
    official_functions = models.TextField(
        null=True, blank=True,
        help_text="Official functions that I hold in national and international programs, commissions, etc.")

    # 11
    upload_photo = models.ImageField(upload_to='media/experts', null=True, blank=True)

    # 12-14
    url_personal = models.URLField(_("Personal website"),
        null=True, blank=True, max_length=1024,
        help_text="Link to personal or professional homepage")
    url_cv = models.URLField(_("Curriculum Vitae"),
        null=True, blank=True, max_length=1024,
        help_text="Link to CV, e.g. on LinkedIn")
    url_researchgate = models.URLField(_("ResearchGate link"),
        null=True, blank=True, max_length=1024,
        help_text="Link to your profile")

    # 15 See https://members.orcid.org/api/workflow/RIM-systems
    orcid = models.CharField(
        _("ORCID"),
        max_length=128, null=True, blank=True, unique=True,
        help_text="ORCID is a persistent unique digital identifier that you own and control")
    proclimid = models.CharField(
        _("ProClim ID"),
        max_length=128, null=True, blank=True, unique=True,
        help_text="Identifier from SCNAT database")

    # 17
    url_publications = models.URLField(
        _("Link to publications"),
        null=True, blank=True, max_length=1024
    )
    list_publications = models.TextField(
        _("Free text list of publications"),
        null=True, blank=True
    )

    # 18-22
    allow_public = models.BooleanField(default=True, help_text="I allow publishing my profile on the web")
    allow_photo = models.BooleanField(default=True, help_text="I allow publishing my photo on the web")

    # 2 EXPERTISE

    @property
    def fullname(self):
        namearray = []
        if self.title: namearray.append(self.title)
        if self.first_name: namearray.append(self.first_name)
        if self.last_name: namearray.append(self.last_name)
        return " ".join(namearray)

    @property
    def publications(self):
        pub = self.list_publications
        return pub.replace('\n', '<br>').replace('¶', '<br>')

    @property
    def location(self):
        if self.affiliation:
            return self.affiliation.location
        else:
            return ""

    @property
    def career(self):
        if self.career_stage == 'OTHER':
            return self.career_stage_note
        return self.get_career_stage_display()

    def __str__(self):
        return self.fullname

    objects = ExpertManager()

    class Meta:
        verbose_name = _('Expert')
        verbose_name_plural = _('Experts')
        unique_together = [['first_name', 'last_name']]

    def natural_key(self):
        return (self.first_name, self.last_name)


# The following is to apply limit on number of affiliations and projects that user can select in their profile

def affiliations_changed(sender, **kwargs):
    if kwargs['instance'].affiliations.count() > 3:
        raise ValidationError("You can't assign more than three affiliations.")

m2m_changed.connect(affiliations_changed, sender=Expert.affiliations.through)
