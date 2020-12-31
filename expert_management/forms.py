from django import forms
from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
from mapwidgets.widgets import GooglePointFieldWidget

from . import data
from .models import Mountain, Project, User, Affiliation


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
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
    expertise = forms.MultipleChoiceField(
        required=False,
        choices=[
            *data.RESEARCH_EXPERTISE, *data.ATMOSPHERIC_SCIENCES_SUBCATEGORIES,
            *data.HYDROSPHERIC_SCIENCES_SUBCATEGORIES, *data.CRYOSPHERIC_SCIENCES_SUBCATEGORIES,
            *data.EARTH_SCIENCES_SUBCATEGORIES, *data.BIOLOGICAL_SCIENCES_SUBCATEGORIES,
            *data.SOCIAL_SCIENCES_AND_HUMANITIES_SUBCATEGORIES, *data.INTEGRATED_SYSTEMS_SUBCATEGORIES,
            *data.SPATIAL_SCALE_OF_EXPERTISE, *data.STATISTICAL_FOCUS, *data.TIME_SCALES,
            *data.METHODS, *data.ASSESSMENT_TYPES, *data.UN_CONVENTIONS_POLICY_PROCESSES
            ]
    )
    regions_of_expertise = forms.ModelChoiceField(
        queryset=Mountain.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}),
        label="Mountain Ranges of Research Expertise", to_field_name="name"
    )


class AdvanceSearchForm(SearchForm):
    regions_of_interest = forms.ModelChoiceField(
        queryset=Mountain.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}),
        label="Mountain Ranges of Research Interest", to_field_name="name"
    )
    career_stage = forms.ChoiceField(
        choices=data.CareerStage.choices, required=False, widget=forms.SelectMultiple(attrs={'multiple': 'multiple'})
    )
    official_functions = forms.CharField(required=False)
    affiliation = forms.ModelChoiceField(
        queryset=Affiliation.objects.all(), widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}),
        required=False, label="Affiliation", to_field_name="name"
    )
    country = CountryField().formfield(required=False, label="Affiliation / Project Country")
