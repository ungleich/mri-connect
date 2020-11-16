from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from django_countries.fields import CountryField
# from django.contrib.gis.db import PointField
from multiselectfield import MultiSelectField

class Affiliation(models.Model):
    name = models.CharField(max_length=256)
    department = models.CharField(max_length=256, null=True, blank=True)
    street = models.CharField(max_length=256, null=True, blank=True)
    post_code = models.CharField(max_length=256, null=True, blank=True)
    city = models.CharField(max_length=256, null=True, blank=True)
    country = CountryField(null=True, blank=True)

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
    funding = models.CharField(max_length=256, null=True, blank=True)
    role = models.CharField(max_length=256, null=True, blank=True)
    homepage = models.URLField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    # TODO: add GeoDjango support
    # coordinates = PointField()
    country = CountryField(null=True, blank=True)
    def __str__(self):
        return self.name

class Topic(models.Model):
    title = models.CharField(max_length=256)
    def __str__(self):
        return self.title
    class Meta:
        verbose_name = _('Topic')
        verbose_name_plural = _('Topics')

class Expertise(models.Model):
    title = models.CharField(max_length=256)
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, null=True, blank=True)
    def __str__(self):
        return self.title
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


class PersonManager(models.Manager):
    def get_by_natural_key(self, first_name, last_name):
        return self.get(first_name=first_name, last_name=last_name)

class Person(models.Model):
    date_added = models.DateField(auto_now_add=True)
    date_edited = models.DateField(auto_now=True)

    # 1-4
    last_name = models.CharField(max_length=128, null=True, blank=True)
    first_name = models.CharField(max_length=128, null=True, blank=True)
    title = models.CharField(max_length=16, null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True,
                              choices=Gender.choices)

    # 5
    position = models.CharField(max_length=256, null=True, blank=True)

    # 6
    affiliation = models.ForeignKey(Affiliation, on_delete=models.PROTECT, null=True, blank=True)

    # 7 Preferred email contact*
    contact_email = models.CharField(max_length=256,
                                    null=True, blank=True,
                                    unique=True)

    # 8 I am..
    career_stage = models.CharField(max_length=16,
                                    null=True, blank=True,
                                    choices=CareerStage.choices)
    # 8
    career_stage_note = models.CharField(_("Other"),
                                    null=True, blank=True,
                                    max_length=256)

    # 9
    career_graduation = models.PositiveIntegerField(
        _("Year of last degree graduation"),
        null=True, blank=True,
        validators=[
            MinValueValidator(1900), MaxValueValidator(2100)
        ])

    # 9.1
    preferences = MultiSelectField(
        choices=PEOPLE_PREFERENCES, null=True, blank=True
    )

    # 10
    official_functions = models.TextField(
        null=True, blank=True,
        help_text="Official functions that I hold in national and international programs, commissions, etc.")

    # 11
    upload_photo = models.ImageField(upload_to='static/people', null=True, blank=True)

    # 12-14
    url_personal = models.URLField(
        _("Personal website"), null=True, blank=True,
        help_text="Link to personal or professional homepage")
    url_cv = models.URLField(
        _("Curriculum Vitae"), null=True, blank=True,
        help_text="Link to CV, e.g. on LinkedIn")
    url_researchgate = models.URLField(
        _("ResearchGate link"), null=True, blank=True,
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

    # 16 Current Projects (note: max 5)
    projects = models.ManyToManyField(Project,
        related_name="experts", blank=True
    )

    # 17
    url_publications = models.URLField(
        _("Link to publications"),
        null=True, blank=True
    )
    list_publications = models.TextField(
        _("Free text list of publications"),
        null=True, blank=True
    )

    # 18-22
    allow_public = models.BooleanField(
        null=True, blank=True,
        help_text="I allow publishing my profile on the web")
    allow_photo = models.BooleanField(
        null=True, blank=True,
        help_text="I allow publishing my photo on the web")

    # 2 EXPERTISE
    expertise = models.ManyToManyField(Expertise,
        related_name="experts", blank=True,
        help_text="Research expertise"
    )

    @property
    def fullname(self):
        namearray = []
        if self.title: namearray.append(self.title)
        if self.first_name: namearray.append(self.first_name)
        if self.last_name: namearray.append(self.last_name)
        return " ".join(namearray)

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

    objects = PersonManager()

    class Meta:
        verbose_name = _('Person')
        verbose_name_plural = _('People')
        unique_together = [['first_name', 'last_name']]

    def natural_key(self):
        return (self.first_name, self.last_name)
