from functools import reduce
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django_countries.fields import CountryField
from mapwidgets.widgets import GooglePointFieldWidget

from . import data
from . import models
from .utils.common import zip_with_itself


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = ("first_name", "last_name", "username", "email", "password1", "password2", "is_subscribed_to_newsletter")


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
            lambda acc, val: acc.union(val.objects.values_list("title")),
            expertise_subcategories,
            models.ResearchExpertise.objects.none()
        )
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
        queryset=models.Affiliation.objects.all(), widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}),
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
