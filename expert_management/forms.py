from functools import reduce
from django import forms
from django.conf import settings

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django_countries.fields import CountryField
from django.forms.widgets import CheckboxSelectMultiple
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, Layout, Field

from mapwidgets.widgets import GooglePointFieldWidget

from . import data
from . import models
from .utils.common import zip_with_itself
from .utils.mailchimp import Mailchimp


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2", "is_subscribed_to_newsletter")

    def save(self, commit=True):
        user = super().save(commit)
        mailchimp = Mailchimp()

        if user.is_subscribed_to_newsletter:
            mailchimp.add_member(user.email, settings.MAILCHIMP_LIST_ID)
        else:
            mailchimp.delete_member(user.email, settings.MAILCHIMP_LIST_ID)

        return user


class ProjectForm(forms.ModelForm):
    class Meta:
        model = models.Project
        exclude = ("user", )
        fields = "__all__"
        widgets = {
            'coordinates': GooglePointFieldWidget,
            'date_start': forms.DateInput(attrs={'type': 'date'}),
            'date_ending': forms.DateInput(attrs={'type': 'date'}),
        }


class ExpertiseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.use_custom_control = False
        self.helper.add_input(Submit("submit", "Submit"))
        self.helper.label_class = "col-form-label col-form-label-lg"
        self.helper.layout = Layout(
            Field('research_expertise'),
            HTML("<hr>"),
            HTML("<h3>Disciplinary Expertise</h3>"),
            Field('atmospheric_sciences'),
            Field('hydrospheric_sciences'),
            Field('cryospheric_sciences'),
            Field('earth_sciences'),
            Field('biological_sciences'),
            Field('social_sciences_and_humanities'),
            Field('integrated_systems'),
            HTML("<hr>"),
            Field('spatial_scale_of_expertise'),
            Field('statistical_focus'),
            Field('time_scales'),
            Field('methods'),
            Field('mountain_ranges_of_research_interest'),
            Field('mountain_ranges_of_research_expertise'),
            Field('participation_in_assessments'),
            Field('inputs_or_participation_to_un_conventions'),
        )

    class Meta:
        model = models.Expertise
        exclude = ("user",)
        widgets = {
            'research_expertise': CheckboxSelectMultiple,
            'atmospheric_sciences': CheckboxSelectMultiple,
            'hydrospheric_sciences': CheckboxSelectMultiple,
            'cryospheric_sciences': CheckboxSelectMultiple,
            'earth_sciences': CheckboxSelectMultiple,
            'biological_sciences': CheckboxSelectMultiple,
            'social_sciences_and_humanities': CheckboxSelectMultiple,
            'integrated_systems': CheckboxSelectMultiple,
            'spatial_scale_of_expertise': CheckboxSelectMultiple,
            'statistical_focus': CheckboxSelectMultiple,
            'time_scales': CheckboxSelectMultiple,
            'methods': CheckboxSelectMultiple,
            'participation_in_assessments': CheckboxSelectMultiple,
            'inputs_or_participation_to_un_conventions': CheckboxSelectMultiple,
        }
        ordering = ['research_expertise__title']


class SearchForm(forms.Form):
    name = forms.CharField(required=False)

    # We are allowing custom choices (on client side) for the expertise field
    # and that would work because we are not validating the submitted form date.
    expertise_subcategories = [
        models.ResearchExpertise, models.AtmosphericSciences, models.HydrosphericSciences, models.CryosphericSciences,
        models.EarthSciences, models.BiologicalSciences, models.SocialSciencesAndHumanities, models.IntegratedSystems,
        models.SpatialScaleOfExpertise, models.StatisticalFocus, models.TimeScales, models.Methods,
        models.ParticipationInAssessments, models.InputsOrParticipationToUNConventions
    ]
    expertise = forms.ModelChoiceField(
        required=False, widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}),
        to_field_name="title",
        queryset = reduce(
            lambda acc, val: acc.union(val.objects.all().exclude(title="Other")),
            expertise_subcategories,
            models.ResearchExpertise.objects.none()
        ).order_by("title")
    )
    regions_of_expertise = forms.ModelChoiceField(
        queryset=models.Mountain.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}),
        label="Mountain Ranges of Research Expertise", to_field_name="name"
    )


class AdvancedSearchForm(SearchForm):
    regions_of_interest = forms.ModelChoiceField(
        queryset=models.Mountain.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}),
        label="Mountain Ranges of Research Interest", to_field_name="name"
    )
    career_stage = forms.ChoiceField(
        choices=data.CareerStage.choices, required=False, widget=forms.SelectMultiple(attrs={'multiple': 'multiple'})
    )
    official_functions = forms.CharField(required=False)
    affiliation = forms.ModelChoiceField(
        queryset=models.Affiliation.objects.all().order_by("name"), widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}),
        required=False, label="Affiliation", to_field_name="name"
    )
    country = CountryField().formfield(required=False, label="Affiliation / Project Country")
    participation_in_assessments = forms.ModelChoiceField(
        queryset=models.ParticipationInAssessments.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'multiple': 'multiple'})
    )
    inputs_or_participation_to_un_conventions = forms.ModelChoiceField(
        label="Inputs / Participation to UN Conventions", queryset=models.InputsOrParticipationToUNConventions.objects.all(),
        required=False, widget=forms.SelectMultiple(attrs={'multiple': 'multiple'})
    )
