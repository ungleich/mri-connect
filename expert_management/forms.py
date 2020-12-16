from django import forms
from mapwidgets.widgets import GooglePointFieldWidget

from .models import Project


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
