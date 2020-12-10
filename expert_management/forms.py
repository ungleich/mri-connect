from mapwidgets.widgets import GooglePointFieldWidget
from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        exclude = ("user", )
        fields = "__all__"
        widgets = {
            'coordinates': GooglePointFieldWidget,
        }
