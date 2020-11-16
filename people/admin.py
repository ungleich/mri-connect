from django.contrib import admin
from .models import Person, Expertise, Topic, Affiliation

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
    # view_template = 'people/admin/preview.html'

@admin.register(Expertise)
class ExpertiseAdmin(admin.ModelAdmin):
    fields = ('title', 'topic')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass

@admin.register(Affiliation)
class AffiliationAdmin(admin.ModelAdmin):
    pass
