# Generated by Django 3.1.4 on 2021-01-13 13:38

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import expert_management.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('date_added', models.DateField(auto_now_add=True)),
                ('date_edited', models.DateField(auto_now=True)),
                ('last_name', models.CharField(max_length=128)),
                ('first_name', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('title', models.CharField(blank=True, choices=[('MR', 'Mr.'), ('MS', 'Ms.'), ('MRS', 'Mrs.'), ('DR', 'Dr.'), ('PROF', 'Prof.'), ('PROF_EMERIT', 'Prof. emerit.')], max_length=16, null=True)),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], max_length=16, null=True)),
                ('position', models.CharField(max_length=256)),
                ('career_stage', models.CharField(blank=True, choices=[('UNDERGRAD', 'Undergraduate student (e.g. BSc/BA)'), ('POSTGRAD', 'Postgraduate student (Masters/PhD student)'), ('POSTDOC', 'Postdoc/Junior Researcher'), ('ACADEMIC', 'Academic (Senior Researcher, Professor)'), ('PUBLICSECTOR', 'Practitioner in the public/government sector'), ('PRIVATESECTOR', 'Practitioner or business in the private sector'), ('OTHER', 'Other (short text)')], max_length=16, null=True, verbose_name='I am ')),
                ('career_stage_note', models.CharField(blank=True, max_length=256, null=True, verbose_name='Other')),
                ('year_of_last_degree_graduation', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2100)], verbose_name='Year of last degree graduation')),
                ('preferences', expert_management.models.MultiSelectField(base_field=models.CharField(choices=[('join_ecr', 'Would you like to join the MRI Early Career Researchers (ECRs) fellows group? (applies to currently enrolled students, practitioners, or postgraduate/postdoctoral scholars up to 5 years since obtaining last degree)'), ('contact_me', 'I allow MRI to contact me regarding my profile, as listed on the database, to link to and promote in its communications channels (website, social media, newsletter article).'), ('expert_registry', 'I would like to be added to an experts registry for internal use by the MRI Coordination Office to identify and connect with external requests for consultancies, expertise, provide inputs for policy briefs/policy reviews, speaking role, or interviews (such as by third parties, journalists or collaborators of the MRI).'), ('newsletter', 'I would like to receive monthly MRI Global Newsletters and Newsflashes from the MRI')], max_length=128), blank=True, default=list, null=True, size=None)),
                ('official_functions', models.TextField(blank=True, help_text='Official functions that I hold in national and international programs, commissions, etc.', null=True)),
                ('photo', models.ImageField(blank=True, null=True, upload_to='experts')),
                ('url_personal', models.URLField(blank=True, help_text='Link to personal or professional homepage', max_length=1024, null=True, verbose_name='Personal website')),
                ('url_cv', models.URLField(blank=True, help_text='Link to CV, e.g. on LinkedIn', max_length=1024, null=True, verbose_name='Curriculum Vitae')),
                ('url_researchgate', models.URLField(blank=True, help_text='Link to your profile', max_length=1024, null=True, verbose_name='ResearchGate link')),
                ('orcid', models.CharField(blank=True, help_text='ORCID is a persistent unique digital identifier that you own and control', max_length=128, null=True, unique=True, verbose_name='ORCID')),
                ('url_publications', models.URLField(blank=True, max_length=1024, null=True, verbose_name='Link to publications')),
                ('list_publications', models.TextField(blank=True, null=True, verbose_name='Free text list of publications')),
                ('is_public', models.BooleanField(default=False, help_text='I allow publishing my profile on the web')),
                ('is_photo_public', models.BooleanField(default=False, help_text='I allow publishing my photo on the web')),
            ],
            options={
                'verbose_name': 'Expert',
                'verbose_name_plural': 'Experts',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Affiliation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=512)),
                ('street', models.CharField(blank=True, max_length=1024, null=True)),
                ('post_code', models.CharField(blank=True, max_length=256, null=True)),
                ('city', models.CharField(blank=True, max_length=256, null=True)),
                ('country', django_countries.fields.CountryField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Mountain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=250)),
                ('mpoly', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('acronym', models.CharField(blank=True, max_length=16, null=True)),
                ('date_start', models.DateField(blank=True, null=True)),
                ('date_ending', models.DateField(blank=True, null=True)),
                ('funding_source', models.CharField(blank=True, max_length=256, null=True)),
                ('role', models.CharField(blank=True, max_length=256, null=True)),
                ('homepage', models.URLField(blank=True, max_length=1024, null=True)),
                ('location', models.CharField(blank=True, help_text='This is the location where the research is conducted or the fieldwork, not the home of research group/affiliation', max_length=256, null=True)),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('country', django_countries.fields.CountryField(blank=True, help_text='This is the country where the research is conducted or the fieldwork, not the home of research group/affiliation', max_length=2, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Expertise',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('research_expertise', expert_management.models.MultiSelectField(base_field=models.CharField(choices=[('Basic Research', 'Basic Research'), ('Applied Research', 'Applied Research'), ('Research Interface and Management', 'Research Interface and Management'), ('Interdisciplinary Research', 'Interdisciplinary Research'), ('Transdisciplinary Research', 'Transdisciplinary Research')], max_length=256), blank=True, default=list, null=True, size=None)),
                ('atmospheric_sciences', expert_management.models.MultiSelectField(base_field=models.CharField(choices=[('Meteorology', 'Meteorology'), ('Climatology', 'Climatology'), ('Atmospheric Physics / Chemistry', 'Atmospheric Physics / Chemistry'), ('Pollution', 'Pollution')], max_length=256), blank=True, default=list, null=True, size=None)),
                ('hydrospheric_sciences', expert_management.models.MultiSelectField(base_field=models.CharField(choices=[('Fresh Water Systems', 'Fresh Water Systems'), ('Precipitation and Runoff', 'Precipitation and Runoff'), ('Hydrogeology', 'Hydrogeology')], max_length=256), blank=True, default=list, null=True, size=None)),
                ('cryospheric_sciences', expert_management.models.MultiSelectField(base_field=models.CharField(choices=[('Glaciology', 'Glaciology'), ('Snow Sciences', 'Snow Sciences'), ('Permafrost and solifluction', 'Permafrost and solifluction')], max_length=256), blank=True, default=list, null=True, size=None)),
                ('earth_sciences', expert_management.models.MultiSelectField(base_field=models.CharField(choices=[('Soil Science/Pedology', 'Soil Science/Pedology'), ('Geomorphology', 'Geomorphology'), ('Geochemistry', 'Geochemistry'), ('Geology', 'Geology'), ('Physical Geography', 'Physical Geography'), ('Geophysics', 'Geophysics')], max_length=256), blank=True, default=list, null=True, size=None)),
                ('biological_sciences', expert_management.models.MultiSelectField(base_field=models.CharField(choices=[('Botany', 'Botany'), ('Zoology', 'Zoology'), ('Ecology', 'Ecology'), ('Terrestrial Ecosystems', 'Terrestrial Ecosystems'), ('Aquatic Ecosystems', 'Aquatic Ecosystems'), ('Soil organisms', 'Soil organisms'), ('Forestry', 'Forestry'), ('Ecosystem functioning', 'Ecosystem functioning'), ('Ecosystem services', 'Ecosystem services'), ('Biodiversity', 'Biodiversity')], max_length=256), blank=True, default=list, null=True, size=None)),
                ('social_sciences_and_humanities', expert_management.models.MultiSelectField(base_field=models.CharField(choices=[('History, classical studies, archaeology, prehistory and early history', 'History, classical studies, archaeology, prehistory and early history'), ('Linguistics and literature, philosophy', 'Linguistics and literature, philosophy'), ('Art studies, musicology, theatre and film studies, architecture', 'Art studies, musicology, theatre and film studies, architecture'), ('Ethnology, social and human geography', 'Ethnology, social and human geography'), ('Psychology', 'Psychology'), ('Educational studies', 'Educational studies'), ('Sociology, social work', 'Sociology, social work'), ('Political sciences', 'Political sciences'), ('Media and communication studies', 'Media and communication studies'), ('Public health', 'Public health'), ('Economics', 'Economics'), ('Law', 'Law')], max_length=256), blank=True, default=list, null=True, size=None)),
                ('integrated_systems', expert_management.models.MultiSelectField(base_field=models.CharField(choices=[('Carbon Cycle', 'Carbon Cycle'), ('Other Biogeochemical Cycles', 'Other Biogeochemical Cycles'), ('Hydrogeochemical Cycle', 'Hydrogeochemical Cycle'), ('Nutrient Cycle', 'Nutrient Cycle'), ('Social-ecological Systems', 'Social-ecological Systems')], max_length=256), blank=True, default=list, null=True, size=None)),
                ('other_expertise', models.TextField(blank=True, help_text='This should be a comma seperated list', null=True)),
                ('spatial_scale_of_expertise', expert_management.models.MultiSelectField(base_field=models.CharField(choices=[('Global / Hemispheric', 'Global / Hemispheric'), ('Continental', 'Continental'), ('Regional', 'Regional'), ('National / Cultural', 'National / Cultural'), ('Local / Community', 'Local / Community')], max_length=256), blank=True, default=list, null=True, size=None)),
                ('other_spatial_scale_of_expertise', models.CharField(blank=True, help_text='This should be a comma seperated list', max_length=1024, null=True)),
                ('statistical_focus', expert_management.models.MultiSelectField(base_field=models.CharField(choices=[('Extremes', 'Extremes'), ('Mean Change / Trends', 'Mean Change / Trends'), ('Variability', 'Variability')], max_length=256), blank=True, default=list, null=True, size=None)),
                ('other_statistical_focus', models.CharField(blank=True, help_text='This should be a comma seperated list', max_length=1024, null=True)),
                ('time_scales', expert_management.models.MultiSelectField(base_field=models.CharField(choices=[('Seasonal / Annual', 'Seasonal / Annual'), ('Decadal / Centennial', 'Decadal / Centennial'), ('Millenial', 'Millenial'), ('100 kyr', '100 kyr'), ('Billenial (Mio yrs)', 'Billenial (Mio yrs)')], max_length=256), blank=True, default=list, null=True, size=None)),
                ('other_time_scales', models.CharField(blank=True, help_text='This should be a comma seperated list', max_length=1024, null=True)),
                ('methods', expert_management.models.MultiSelectField(base_field=models.CharField(choices=[('Earth Observations', 'Earth Observations'), ('Remote sensing', 'Remote sensing'), ('Field observations', 'Field observations'), ('Field Experiments', 'Field Experiments'), ('Modeling', 'Modeling'), ('Spatial analyses', 'Spatial analyses'), ('Policy Analysis', 'Policy Analysis'), ('Qualitative social science methods', 'Qualitative social science methods'), ('Integrative assessments', 'Integrative assessments'), ('Synthesis and meta-analyses', 'Synthesis and meta-analyses')], max_length=256), blank=True, default=list, null=True, size=None)),
                ('other_methods', models.CharField(blank=True, help_text='This should be a comma seperated list', max_length=1024, null=True)),
                ('participation_in_assessments', expert_management.models.MultiSelectField(base_field=models.CharField(choices=[('IPCC', 'IPCC'), ('IPBES', 'IPBES'), ('UNDRR GAR', 'UNDRR GAR')], max_length=256), blank=True, default=list, null=True, size=None)),
                ('other_participation_in_assessments', models.CharField(blank=True, help_text='This should be a comma seperated list', max_length=1024, null=True)),
                ('more_detail_about_participation_in_assessments', models.TextField(blank=True, null=True)),
                ('inputs_or_participation_to_un_conventions', expert_management.models.MultiSelectField(base_field=models.CharField(choices=[('UN Agenda 2030 (SDGs) / UN HLPF', 'UN Agenda 2030 (SDGs) / UN HLPF'), ('UNFCCC', 'UNFCCC'), ('CBD', 'CBD'), ('UNDRR Sedai', 'UNDRR Sedai'), ('UNCCD', 'UNCCD')], max_length=256), blank=True, default=list, null=True, size=None)),
                ('other_inputs_or_participation_to_un_conventions', models.CharField(blank=True, help_text='This should be a comma seperated list', max_length=1024, null=True)),
                ('other_mountain_ranges_of_research_interest', models.TextField(blank=True, null=True)),
                ('other_mountain_ranges_of_research_expertise', models.TextField(blank=True, null=True)),
                ('mountain_ranges_of_research_expertise', models.ManyToManyField(blank=True, related_name='_expertise_mountain_ranges_of_research_expertise_+', to='expert_management.Mountain')),
                ('mountain_ranges_of_research_interest', models.ManyToManyField(blank=True, related_name='_expertise_mountain_ranges_of_research_interest_+', to='expert_management.Mountain')),
                ('user', models.OneToOneField(help_text='Research expertise', on_delete=django.db.models.deletion.CASCADE, related_name='expertise', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Expertise',
                'verbose_name_plural': 'Expertise',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='affiliations',
            field=models.ManyToManyField(blank=True, help_text='Upto 3 affiliations can be added.', related_name='user', to='expert_management.Affiliation'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
