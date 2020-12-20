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

search_form_choices = [(mountain.name, mountain.name) for mountain in Mountain.objects.all()]
search_form_choices.append(("", ""))

class SearchForm(forms.Form):
    name = forms.CharField(required=False)
    expertise = forms.CharField(required=False)
    regions = forms.ChoiceField(choices=search_form_choices, required=False, widget=forms.SelectMultiple(attrs={'multiple': 'multiple'}))
