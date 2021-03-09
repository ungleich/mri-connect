from django.contrib import admin
from django.contrib.gis.db.models import ManyToManyField, PointField
from django.forms.widgets import CheckboxSelectMultiple

from . import models

# from mapwidgets.widgets import GooglePointFieldWidget



@admin.register(models.Expertise)
class ExpertiseAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'research_expertise',
                'spatial_scale_of_expertise',
                'other_spatial_scale_of_expertise',
                'statistical_focus',
                'other_statistical_focus',
                'time_scales',
                'other_time_scales',
                'methods',
                'other_methods',
                'participation_in_assessments',
                'other_participation_in_assessments',
                'more_detail_about_participation_in_assessments',
                'inputs_or_participation_to_un_conventions',
                'other_inputs_or_participation_to_un_conventions',
                'mountain_ranges_of_research_expertise',
                'other_mountain_ranges_of_research_expertise',
                'mountain_ranges_of_research_interest',
                'other_mountain_ranges_of_research_interest',
                'user',
            ]
        }),
        ('Disciplinary Expertise', {
            'fields': [
                'atmospheric_sciences',
                'hydrospheric_sciences',
                'cryospheric_sciences',
                'earth_sciences',
                'biological_sciences',
                'social_sciences_and_humanities',
                'integrated_systems',
            ]
        })
    ]


class ExpertiseInlineAdmin(admin.StackedInline):
    model = models.Expertise

    formfield_overrides = {
        ManyToManyField: {"widget": CheckboxSelectMultiple}
    }

class ProjectInlineAdmin(admin.StackedInline):
    model = models.Project
    exclude = ["coordinates"]
    # formfield_overrides = {
    #     PointField: {"widget": GooglePointFieldWidget}
    # }


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    search_fields = ('first_name', 'last_name', 'username', 'email')
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
    exclude = ["coordinates"]
    # formfield_overrides = {
    #     PointField: {"widget": GooglePointFieldWidget}
    # }


@admin.register(models.GeoMountainsRegistry)
class GeoMountainsRegistryAdmin(admin.ModelAdmin):
    search_fields = ('user__first_name', 'user__last_name', 'user__username', 'user__email')


admin.site.register(models.Mountain)

admin.site.register(models.RoleAndInvolvement)

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
admin.site.register(models.SpamFilterWord)
