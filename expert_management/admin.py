from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.db import models
from mapwidgets.widgets import GooglePointFieldWidget

from .models import Affiliation, Expertise, Project, User


class ExpertiseInlineAdmin(admin.StackedInline):
    model = Expertise


class ProjectInlineAdmin(admin.StackedInline):
    model = Project

    formfield_overrides = {
        models.PointField: {"widget": GooglePointFieldWidget}
    }


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    inlines = (ExpertiseInlineAdmin, ProjectInlineAdmin)


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
