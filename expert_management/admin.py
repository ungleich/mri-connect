from django.contrib import admin
from django.contrib.gis.db import models
from mapwidgets.widgets import GooglePointFieldWidget

from .models import Affiliation, Expert, Expertise, Project


class ExpertiseInlineAdmin(admin.StackedInline):
    model = Expertise


@admin.register(Expert)
class ExpertAdmin(admin.ModelAdmin):
    fieldsets = (
        ('User', {
            'fields': ('user',)
        }),
        ('Expert', {
            'fields': ('last_name', 'first_name', 'title', 'gender')
        }),
        ('Position', {
            'fields': ('position', 'affiliations', 'contact_email')
        }),
        ('Career', {
            'fields': ('career_stage', 'career_stage_note', 'year_of_last_degree_graduation')
        }),
        ('Preferences', {
            'fields': ('preferences', 'official_functions', 'upload_photo')
        }),
        ('Links', {
            'fields': ('url_personal', 'url_cv', 'url_researchgate', 'orcid')
        }),
        ('References', {
            'fields': ('url_publications', 'list_publications')
        }),
        ('Permissions', {
            'fields': ('allow_public', 'allow_photo')
        }),
    )
    search_fields = ('last_name', 'first_name', 'contact_email')
    list_display = ('fullname', 'allow_public', 'date_edited')
    ordering = ('-date_edited',)
    inlines = (ExpertiseInlineAdmin,)

    # view_template = 'expert_management/admin/preview.html'
    class Media:
        css = { 'all': ('admin.css', )}


@admin.register(Expertise)
class ExpertiseAdmin(admin.ModelAdmin):
    ordering = ('id',)


@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    ordering = ('name',)
    search_fields = ('name', 'city',)
    list_display = ('name', 'city', 'country')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    ordering = ('-date_ending',)
    search_fields = ('name', 'location',)
    list_display = ('name', 'date_ending', 'location')

    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }
