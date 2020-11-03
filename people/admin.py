from ra.admin.admin import ra_admin_site, EntityAdmin
from django.contrib.admin import ModelAdmin

from .models import Person, Expertise, Topic


class PersonAdmin(ModelAdmin):
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
            'fields': ('expertise', 'disciplines')
        }),
    )
    # view_template = 'people/admin/preview.html'

class ExpertiseAdmin(EntityAdmin):
    fields = ('title', 'topic')

class TopicAdmin(EntityAdmin):
    pass

ra_admin_site.register(Person, PersonAdmin)
ra_admin_site.register(Expertise, ExpertiseAdmin)
ra_admin_site.register(Topic, TopicAdmin)
