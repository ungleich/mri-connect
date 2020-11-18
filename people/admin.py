from django.contrib import admin
from .models import Person, Expertise, Topic, Affiliation, Project

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Person', {
            'fields': ('last_name', 'first_name', 'title', 'gender')
        }),
        ('Position', {
            'fields': ('position', 'affiliation', 'contact_email')
        }),
        ('Career', {
            'fields': ('career_stage', 'career_stage_note', 'career_graduation')
        }),
        ('Preferences', {
            'fields': ('preferences', 'official_functions', 'upload_photo')
        }),
        ('Links', {
            'fields': ('url_personal', 'url_cv', 'url_researchgate', 'orcid')
        }),
        ('References', {
            'fields': ('projects', 'url_publications', 'list_publications')
        }),
        ('Permissions', {
            'fields': ('allow_public', 'allow_photo')
        }),
        ('Expertise', {
            'fields': ('expertise', )
        }),
    )
    search_fields = ('last_name', 'first_name', 'contact_email')
    list_display = ('fullname', 'allow_public', 'date_edited')
    ordering = ('-date_edited',)
    # view_template = 'people/admin/preview.html'
    class Media:
        css = { 'all': ('admin.css', )}

@admin.register(Expertise)
class ExpertiseAdmin(admin.ModelAdmin):
    fields = ('title', 'topic')
    ordering = ('id',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    ordering = ('id',)

@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    ordering = ('name',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    ordering = ('-date_ending',)
