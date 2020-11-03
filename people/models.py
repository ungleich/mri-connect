from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField
# from django.contrib.gis.db import PointField
from multiselectfield import MultiSelectField

class Affiliation(models.Model):
    name = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    street = models.CharField(max_length=256)
    post_code = models.CharField(max_length=256)
    city = models.CharField(max_length=256)
    country = CountryField()

class Project(models.Model):
    name = models.CharField(max_length=256)
    acronym = models.CharField(max_length=16)
    date_start = models.DateField()
    date_ending = models.DateField()
    funding = models.CharField(max_length=256)
    role = models.CharField(max_length=256)
    homepage = models.URLField()
    location = models.TextField()
    # TODO: add GeoDjango support
    # coordinates = PointField()
    country = CountryField()

class Topic(models.Model):
    title = models.CharField(max_length=256)
    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

class Expertise(models.Model):
    title = models.CharField(max_length=256)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, null=True, blank=True)
    class Meta:
        verbose_name = _('Expertise')
        verbose_name_plural = _('Expertise')

class Title(models.TextChoices):
    MS = 'Ms.'
    MRS = 'Mrs.'
    DR = 'Dr.'
    PROF = 'Prof.'
    PROFEM = 'Prof. em.'

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

PEOPLE_PREFERENCES = (
    ('join_ecr', _("Would you like to join the MRI Early Career Researchers (ECRs) fellows group? (applies to currently enrolled students, practitioners, or postgraduate/postdoctoral scholars up to 5 years since obtaining last degree)")),
    ('contact_me', _("I allow MRI to contact me regarding my profile, as listed on the database, to link to and promote in its communications channels (website, social media, newsletter article).")),
    ('expert_registry', _("I would like to be added to an experts registry for internal use by the MRI Coordination Office to identify and connect with external requests for consultancies, expertise, provide inputs for policy briefs/policy reviews, speaking role, or interviews (such as by third parties, journalists or collaborators of the MRI).")),
    ('newsletter', _("I would like to receive monthly MRI Global Newsletters and Newsflashes from the MRI")),
)

class Person(models.Model):
    date_added = models.DateField(auto_now_add=True)
    date_edited = models.DateField(auto_now=True)

    # 1-4
    last_name = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    title = models.CharField(max_length=16)
    gender = models.CharField(max_length=1,
                              choices=Gender.choices)

    # 5
    position = models.CharField(max_length=256)

    # 6
    affiliation = models.ForeignKey(Affiliation, on_delete=models.PROTECT, null=True, blank=True)

    # 7 Preferred email contact*
    contact_email = models.CharField(max_length=256)

    # 8 I am..
    career_stage = models.CharField(max_length=16,
                                    choices=CareerStage.choices)
    # 8
    career_stage_note = models.CharField(_("Other"), max_length=256)

    # 9
    career_graduation = models.PositiveIntegerField(
        _("Year of last degree graduation"),
        validators=[
            MinValueValidator(1900), MaxValueValidator(2100)
        ])

    # 9.1
    preferences = MultiSelectField(
        choices=PEOPLE_PREFERENCES
    )

    # 10
    official_functions = models.TextField(
        help_text="Official functions that I hold in national and international programs, commissions, etc.")

    # 11
    upload_photo = models.FileField()

    # 12-14
    url_personal = models.URLField(
        _("Personal website"),
        help_text="Link to personal or professional homepage")
    url_cv = models.URLField(
        _("Curriculum Vitae"),
        help_text="Link to CV, e.g. on LinkedIn")
    url_researchgate = models.URLField(
        _("ResearchGate link"),
        help_text="Link to your profile")

    # 15 See https://members.orcid.org/api/workflow/RIM-systems
    orcid = models.CharField(
        _("ORCID"),
        max_length=128, unique=True,
        help_text="ORCID is a persistent unique digital identifier that you own and control")

    # 16 Current Projects (note: max 5)
    projects = models.ManyToManyField(Project,
        related_name="experts",
    )

    # 17
    url_publications = models.URLField(
        _("Link to publications")
    )
    list_publications = models.TextField(
        _("Free text list of publications")
    )

    # 18-22
    allow_public = models.BooleanField(
        help_text="I allow publishing my profile on the web")
    allow_photo = models.BooleanField(
        help_text="I allow publishing my photo on the web")

    expertise = models.ManyToManyField(Expertise,
        related_name="experts",
        help_text="Research expertise"
    )

    disciplines = models.ManyToManyField(Topic,
        related_name="experts",
        help_text="Disciplinary expertise topics"
    )

    @property
    def fullname(self):
        namearray = []
        if self.title: namearray.push(self.title)
        if self.first_name: namearray.push(self.first_name)
        if self.last_name: namearray.push(self.last_name)
        return " ".join(namearray)

    class Meta:
        verbose_name = _('Expert')
        verbose_name_plural = _('Experts')
