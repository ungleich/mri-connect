from django.contrib import admin
from django.contrib.gis.db.models import PointField, ManyToManyField
from django.forms.widgets import CheckboxSelectMultiple
from mapwidgets.widgets import GooglePointFieldWidget

from . import models


class ExpertiseInlineAdmin(admin.StackedInline):
    model = models.Expertise

    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple}
    }

class ProjectInlineAdmin(admin.StackedInline):
    model = models.Project

    formfield_overrides = {
        PointField: {"widget": GooglePointFieldWidget}
    }


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name')
    inlines = (ExpertiseInlineAdmin, ProjectInlineAdmin)


@admin.register(models.Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name', 'city',)
    list_display = ('name', 'city', 'country')


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    ordering = ('-date_ending',)
    search_fields = ('name', 'location',)
    list_display = ('name', 'date_ending', 'location')

    formfield_overrides = {
        PointField: {"widget": GooglePointFieldWidget}
    }

admin.site.register(models.Mountain)

admin.site.register(models.RoleAndInvolvement)
admin.site.register(models.GeoMountainsRegistry)

admin.site.register(models.DisciplinaryExpertise)
admin.site.register(models.ResearchExpertise)
admin.site.register(models.AtmosphericSciences)
admin.site.register(models.HydrosphericSciences)
admin.site.register(models.CryosphericSciences)
admin.site.register(models.EarthSciences)
admin.site.register(models.BiologicalSciences)
admin.site.register(models.SocialSciencesAndHumanities)
admin.site.register(models.IntegratedSystems)
admin.site.register(models.SpatialScaleOfExpertise)
admin.site.register(models.StatisticalFocus)
admin.site.register(models.TimeScales)
admin.site.register(models.Methods)
admin.site.register(models.ParticipationInAssessments)
admin.site.register(models.InputsOrParticipationToUNConventions)
