import random

from functools import reduce
from django import forms
from django.conf import settings

from django.contrib.auth.forms import UserCreationForm
from django_countries.fields import CountryField
from django.forms import ValidationError
from django.forms.widgets import CheckboxSelectMultiple
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, Layout, Field

from mapwidgets.widgets import GooglePointFieldWidget

from . import data
from . import models
from .utils.mailchimp import Mailchimp


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = models.User
        fields = (
            "first_name", "last_name", "username", "email", "password1", "password2", "is_subscribed_to_newsletter"
        )

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
            Field('other_atmospheric_sciences'),

            Field('biological_sciences'),
            Field('other_biological_sciences'),

            Field('cryospheric_sciences'),
            Field('other_cryospheric_sciences'),

            Field('earth_sciences'),
            Field('other_earth_sciences'),

            Field('hydrospheric_sciences'),
            Field('other_hydrospheric_sciences'),

            Field('integrated_systems'),
            Field('other_integrated_systems'),

            Field('social_sciences_and_humanities'),

            Field('other_social_sciences_and_humanities'),

            HTML("<hr>"),

            Field('inputs_or_participation_to_un_conventions'),
            Field('other_inputs_or_participation_to_un_conventions'),

            Field('methods'),
            Field('other_methods'),

            Field('mountain_ranges_of_research_expertise'),
            Field('other_mountain_ranges_of_research_expertise'),

            Field('mountain_ranges_of_research_interest'),
            Field('other_mountain_ranges_of_research_interest'),

            Field('participation_in_assessments'),
            Field('other_participation_in_assessments'),
            Field('more_detail_about_participation_in_assessments'),

            Field('spatial_scale_of_expertise'),
            Field('other_spatial_scale_of_expertise'),

            Field('statistical_focus'),
            Field('other_statistical_focus'),

            Field('time_scales'),
            Field('other_time_scales'),
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.use_custom_control = False
        self.helper.add_input(Submit("search", "Search"))
        self.helper.label_class = "col-form-label"

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
    mountain_ranges_of_research_expertise = forms.ModelChoiceField(
        queryset=models.Mountain.objects.all(), required=False,
        widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}),
        label="Mountain Ranges of Research Expertise", to_field_name="name"
    )


class AdvancedSearchForm(SearchForm):
    expertise = None
    mountain_ranges_of_research_interest = forms.ModelChoiceField(
        queryset=models.Mountain.objects.all(), required=False,
        widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}),
        label="Mountain Ranges of Research Interest", to_field_name="name"
    )

    research_expertise = forms.ModelChoiceField(
        queryset=models.ResearchExpertise.objects.all(), required=False,
        widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}), to_field_name="title"
    )
    atmospheric_sciences = forms.ModelChoiceField(
        queryset=models.AtmosphericSciences.objects.all(), required=False,
        widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}), to_field_name="title"
    )
    hydrospheric_sciences = forms.ModelChoiceField(
        queryset=models.HydrosphericSciences.objects.all(), required=False,
        widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}), to_field_name="title"
    )
    cryospheric_sciences = forms.ModelChoiceField(
        queryset=models.CryosphericSciences.objects.all(), required=False,
        widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}), to_field_name="title"
    )
    earth_sciences = forms.ModelChoiceField(
        queryset=models.EarthSciences.objects.all(), required=False,
        widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}), to_field_name="title"
    )
    biological_sciences = forms.ModelChoiceField(
        queryset=models.BiologicalSciences.objects.all(), required=False,
        widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}), to_field_name="title"
    )
    social_sciences_and_humanities = forms.ModelChoiceField(
        queryset=models.SocialSciencesAndHumanities.objects.all(), required=False,
        widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}), to_field_name="title"
    )
    integrated_systems = forms.ModelChoiceField(
        queryset=models.IntegratedSystems.objects.all(), required=False,
        widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}), to_field_name="title"
    )
    spatial_scale_of_expertise = forms.ModelChoiceField(
        queryset=models.SpatialScaleOfExpertise.objects.all(), required=False,
        widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}), to_field_name="title"
    )
    statistical_focus = forms.ModelChoiceField(
        queryset=models.StatisticalFocus.objects.all(), required=False,
        widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}), to_field_name="title"
    )
    time_scales = forms.ModelChoiceField(
        queryset=models.TimeScales.objects.all(), required=False,
        widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}), to_field_name="title"
    )
    methods = forms.ModelChoiceField(
        queryset=models.Methods.objects.all(), required=False,
        widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}), to_field_name="title"
    )
    participation_in_assessments = forms.ModelChoiceField(
        queryset=models.ParticipationInAssessments.objects.all(), required=False,
        widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}), to_field_name="title"
    )
    inputs_or_participation_to_un_conventions = forms.ModelChoiceField(
        queryset=models.InputsOrParticipationToUNConventions.objects.all(), required=False,
        widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}), to_field_name="title",
        label="Inputs / Participation to United Nations Conventions"
    )
    other_expertise = forms.CharField(required=False)

    career_stage = forms.ChoiceField(
        choices=data.CareerStage.choices, required=False, widget=forms.SelectMultiple(attrs={'multiple': 'multiple'})
    )
    official_functions = forms.CharField(required=False)
    affiliation = forms.ModelChoiceField(
        queryset=models.Affiliation.objects.all().order_by("name"), required=False, label="Affiliation",
        to_field_name="name", widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}),

    )
    country = CountryField().formfield(required=False, label="Affiliation / Project Country")


class CaptchaField(forms.ChoiceField):
    #TODO: We should movie the choices inside the CaptchaField
    #      but I don't see a way to do it dynamically i.e the choices
    #      are updated everytime
    def __init__(self, *args, **kwargs):
        kwargs["label"] = "Prove you are a human! Select the item which is not a mountain, but a Swiss cheese."
        super().__init__(*args, **kwargs)

    def clean(self, value):
        try:
            models.SpamFilterWord.objects.get(text=value)
        except models.SpamFilterWord.DoesNotExist:
            raise ValidationError("Incorrect value selected", "invalid")
        else:
            return value


class ContactForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.use_custom_control = False
        self.helper.add_input(Submit("", "Email"))
        self.helper.label_class = "col-form-label"
        self.fields['captcha'].choices = (
            [(mountain.name, mountain.name) for mountain in models.Mountain.objects.random(3)] +
            [(word.text, word.text) for word in models.SpamFilterWord.objects.random(1)]
        )
        random.shuffle(self.fields['captcha'].choices)


    email = forms.EmailField(required=True, label="Your Email")
    body = forms.CharField(widget=forms.Textarea, required=True, label="Message")
    captcha = CaptchaField()
