from django import forms
from django.contrib.auth.forms import UserCreationForm
from mapwidgets.widgets import GooglePointFieldWidget

from .models import Project, User, Mountain


class UserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "contact_email")


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
    expertise = forms.CharField(required=False)
    regions = forms.ModelChoiceField(
        queryset=Mountain.objects.all(), required=False, widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}),
        label="Mountain Ranges of Research Expertise", to_field_name="name"
    )
