from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import m2m_changed
from django.forms import MultipleChoiceField
from django.forms.widgets import CheckboxSelectMultiple
from django.utils.translation import ugettext_lazy as _
from django_countries.fields import CountryField

from . import data
from .utils.common import join_true_values


class MultiSelectField(ArrayField):
    class MyMultipleChoiceField(MultipleChoiceField):
        widget = CheckboxSelectMultiple

    def formfield(self, **kwargs):
        defaults = {
            "form_class": self.MyMultipleChoiceField,
            "choices": self.base_field.choices,
        }
        defaults.update(kwargs)
        return super(ArrayField, self).formfield(**defaults)


class User(AbstractUser):
    date_added = models.DateField(auto_now_add=True)
    date_edited = models.DateField(auto_now=True)

    last_name = models.CharField(max_length=128, null=False, blank=False)
    first_name = models.CharField(max_length=128, null=False, blank=False)

    email = models.EmailField(null=False, blank=False, unique=True)

    title = models.CharField(max_length=16, null=True, blank=True, choices=data.Title.choices)
    gender = models.CharField(max_length=16, null=True, blank=True, choices=data.Gender.choices)

    position = models.CharField(max_length=256, null=False, blank=False)

    affiliations = models.ManyToManyField(
        "Affiliation", related_name="user", blank=True, help_text="Upto 3 affiliations can be added."
    )

    career_stage = models.CharField(
        max_length=16, null=True, blank=True, choices=data.CareerStage.choices, verbose_name="I am "
    )
    career_stage_note = models.CharField(_("Other"), null=True, blank=True, max_length=256)

    year_of_last_degree_graduation = models.PositiveIntegerField(
        _("Year of last degree graduation"),
        null=True,
        blank=True,
        validators=[MinValueValidator(1900), MaxValueValidator(2100)],
    )

    preferences = MultiSelectField(
        models.CharField(choices=data.EXPERTS_PREFERENCES, max_length=128), default=list, null=True, blank=True
    )

    official_functions = models.TextField(
        null=True,
        blank=True,
        help_text="Official functions that I hold in national and international programs, commissions, etc.",
    )

    photo = models.ImageField(upload_to="experts", null=True, blank=True)

    url_personal = models.URLField(
        _("Personal website"),
        null=True,
        blank=True,
        max_length=1024,
        help_text="Link to personal or professional homepage",
    )
    url_cv = models.URLField(
        _("Curriculum Vitae"), null=True, blank=True, max_length=1024, help_text="Link to CV, e.g. on LinkedIn"
    )
    url_researchgate = models.URLField(
        _("ResearchGate link"), null=True, blank=True, max_length=1024, help_text="Link to your profile"
    )

    orcid = models.CharField(
        _("ORCID"),
        max_length=128,
        null=True,
        blank=True,
        unique=True,
        help_text="ORCID is a persistent unique digital identifier that you own and control",
    )

    url_publications = models.URLField(_("Link to publications"), null=True, blank=True, max_length=1024)
    list_publications = models.TextField(_("Free text list of publications"), null=True, blank=True)

    is_public = models.BooleanField(default=False, help_text="I allow publishing my profile on the web")
    is_photo_public = models.BooleanField(default=False, help_text="I allow publishing my photo on the web")

    # 2 EXPERTISE

    @property
    def fullname(self):
        namearray = []
        if self.title:
            namearray.append(self.title)
        if self.first_name:
            namearray.append(self.first_name)
        if self.last_name:
            namearray.append(self.last_name)
        return " ".join(namearray)


    @property
    def publications(self):
        pub = self.list_publications
        return pub.replace("\n", "<br>").replace("¶", "<br>")

    @property
    def career(self):
        if self.career_stage == "OTHER":
            return self.career_stage_note
        return self.get_career_stage_display()

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("Expert")
        verbose_name_plural = _("Experts")


class Affiliation(models.Model):
    name = models.CharField(max_length=512, null=False, blank=False)
    street = models.CharField(max_length=1024, null=True, blank=True)
    post_code = models.CharField(max_length=256, null=True, blank=True)
    city = models.CharField(max_length=256, null=True, blank=True)
    country = CountryField(null=False, blank=False)

    @property
    def location(self):
        if not self.city:
            return self.country.name or ""
        if not self.country:
            return self.city or ""
        return ", ".join([self.city.strip(), self.country.name])

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=256)
    acronym = models.CharField(max_length=16, null=True, blank=True)
    date_start = models.DateField(null=True, blank=True)
    date_ending = models.DateField(null=True, blank=True)
    funding_source = models.CharField(max_length=256, null=True, blank=True)
    role = models.CharField(max_length=256, null=True, blank=True)
    homepage = models.URLField(null=True, blank=True, max_length=1024)
    location = models.CharField(
        max_length=256,
        null=True,
        blank=True,
        help_text="This is the location where the research is conducted or the fieldwork, not the home of research group/affiliation",
    )
    coordinates = models.PointField(null=True, blank=True)
    country = CountryField(
        null=True,
        blank=True,
        help_text="This is the country where the research is conducted or the fieldwork, not the home of research group/affiliation",
    )

    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="projects")

    def __str__(self):
        return self.name


# GMBA Mountains
class Mountain(models.Model):
    name = models.CharField(max_length=50)
    country = models.CharField(max_length=250)
    mpoly = models.MultiPolygonField()

    def __str__(self):
        return f"{self.name}, {self.country}"


class Expertise(models.Model):
    research_expertise = MultiSelectField(
        models.CharField(choices=data.RESEARCH_EXPERTISE, max_length=256), default=list, null=True, blank=True
    )

    atmospheric_sciences = MultiSelectField(
        models.CharField(choices=data.ATMOSPHERIC_SCIENCES_SUBCATEGORIES, max_length=256),
        default=list,
        null=True,
        blank=True,
    )
    hydrospheric_sciences = MultiSelectField(
        models.CharField(choices=data.HYDROSPHERIC_SCIENCES_SUBCATEGORIES, max_length=256),
        default=list,
        null=True,
        blank=True,
    )
    cryospheric_sciences = MultiSelectField(
        models.CharField(choices=data.CRYOSPHERIC_SCIENCES_SUBCATEGORIES, max_length=256),
        default=list,
        null=True,
        blank=True,
    )
    earth_sciences = MultiSelectField(
        models.CharField(choices=data.EARTH_SCIENCES_SUBCATEGORIES, max_length=256), default=list, null=True, blank=True
    )
    biological_sciences = MultiSelectField(
        models.CharField(choices=data.BIOLOGICAL_SCIENCES_SUBCATEGORIES, max_length=256),
        default=list,
        null=True,
        blank=True,
    )
    social_sciences_and_humanities = MultiSelectField(
        models.CharField(choices=data.SOCIAL_SCIENCES_AND_HUMANITIES_SUBCATEGORIES, max_length=256),
        default=list,
        null=True,
        blank=True,
    )
    integrated_systems = MultiSelectField(
        models.CharField(choices=data.INTEGRATED_SYSTEMS_SUBCATEGORIES, max_length=256),
        default=list,
        null=True,
        blank=True,
    )
    other_expertise = models.TextField(null=True, blank=True, help_text="This should be a comma seperated list")

    spatial_scale_of_expertise = MultiSelectField(
        models.CharField(choices=data.SPATIAL_SCALE_OF_EXPERTISE, max_length=256), default=list, null=True, blank=True
    )
    other_spatial_scale_of_expertise = models.CharField(
        max_length=1024, null=True, blank=True, help_text="This should be a comma seperated list"
    )

    statistical_focus = MultiSelectField(
        models.CharField(choices=data.STATISTICAL_FOCUS, max_length=256), default=list, null=True, blank=True
    )
    other_statistical_focus = models.CharField(
        max_length=1024, null=True, blank=True, help_text="This should be a comma seperated list"
    )

    time_scales = MultiSelectField(
        models.CharField(choices=data.TIME_SCALES, max_length=256), default=list, null=True, blank=True
    )
    other_time_scales = models.CharField(
        max_length=1024, null=True, blank=True, help_text="This should be a comma seperated list"
    )

    methods = MultiSelectField(
        models.CharField(choices=data.METHODS, max_length=256), default=list, null=True, blank=True
    )
    other_methods = models.CharField(
        max_length=1024, null=True, blank=True, help_text="This should be a comma seperated list"
    )

    participation_in_assessments = MultiSelectField(
        models.CharField(choices=data.ASSESSMENT_TYPES, max_length=256), default=list, null=True, blank=True
    )
    other_participation_in_assessments = models.CharField(
        max_length=1024, null=True, blank=True, help_text="This should be a comma seperated list"
    )
    more_detail_about_participation_in_assessments = models.TextField(null=True, blank=True)

    inputs_or_participation_to_un_conventions = MultiSelectField(
        models.CharField(choices=data.UN_CONVENTIONS_POLICY_PROCESSES, max_length=256),
        default=list,
        null=True,
        blank=True,
    )
    other_inputs_or_participation_to_un_conventions = models.CharField(
        max_length=1024, null=True, blank=True, help_text="This should be a comma seperated list"
    )

    mountain_ranges_of_research_interest = models.ManyToManyField(Mountain, blank=True, related_name="+")
    other_mountain_ranges_of_research_interest = models.TextField(null=True, blank=True)

    mountain_ranges_of_research_expertise = models.ManyToManyField(Mountain, blank=True, related_name="+")
    other_mountain_ranges_of_research_expertise = models.TextField(null=True, blank=True)

    user = models.OneToOneField(
        User, help_text="Research expertise", on_delete=models.CASCADE, related_name="expertise"
    )

    @property
    def research_expertise_display(self):
        return ", ".join(self.research_expertise)

    @property
    def atmospheric_sciences_display(self):
        return ", ".join(self.atmospheric_sciences)

    @property
    def hydrospheric_sciences_display(self):
        return ", ".join(self.hydrospheric_sciences)

    @property
    def cryospheric_sciences_display(self):
        return ", ".join(self.cryospheric_sciences)

    @property
    def earth_sciences_display(self):
        return ", ".join(self.earth_sciences)

    @property
    def biological_sciences_display(self):
        return ", ".join(self.biological_sciences)

    @property
    def social_sciences_and_humanities_display(self):
        return ", ".join(self.social_sciences_and_humanities)

    @property
    def integrated_systems_display(self):
        return ", ".join(self.integrated_systems)

    @property
    def spatial_scale_of_expertise_display(self):
        return join_true_values([", ".join(self.spatial_scale_of_expertise), self.other_spatial_scale_of_expertise])

    @property
    def statistical_focus_display(self):
        return join_true_values([", ".join(self.statistical_focus), self.other_statistical_focus])

    @property
    def time_scales_display(self):
        return join_true_values([", ".join(self.time_scales), self.other_time_scales])

    @property
    def methods_display(self):
        return join_true_values([", ".join(self.methods), self.other_methods])

    @property
    def participation_in_assessments_display(self):
        return join_true_values([", ".join(self.participation_in_assessments), self.other_participation_in_assessments])

    @property
    def inputs_or_participation_to_un_conventions_display(self):
        return join_true_values(
            [
                ", ".join(self.inputs_or_participation_to_un_conventions),
                self.other_inputs_or_participation_to_un_conventions,
            ]
        )

    @property
    def mountain_ranges_of_research_interest_display(self):
        return join_true_values(
            [
                ", ".join([mountain.name for mountain in self.mountain_ranges_of_research_interest.all()]),
                self.other_mountain_ranges_of_research_interest,
            ]
        )

    @property
    def mountain_ranges_of_research_expertise_display(self):
        return join_true_values(
            [
                ", ".join([mountain.name for mountain in self.mountain_ranges_of_research_expertise.all()]),
                self.other_mountain_ranges_of_research_expertise,
            ]
        )

    def __str__(self):
        return f"{self.user}'s expertise"

    class Meta:
        verbose_name = _("Expertise")
        verbose_name_plural = _("Expertise")


# The following is to apply limit on number of affiliations and projects that user can select in their profile
def affiliations_changed(sender, **kwargs):
    if kwargs["instance"].affiliations.count() > 3:
        raise ValidationError("You can't assign more than three affiliations.")


m2m_changed.connect(affiliations_changed, sender=get_user_model().affiliations.through)
