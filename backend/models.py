# -*- coding: utf-8 -*-

from . import db, Config
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import ImageUploadField
from werkzeug.utils import secure_filename
import enum

organisation_people = db.Table(
    'organisation_people',
    db.Column('person_id', db.Integer(), db.ForeignKey('person.id')),
    db.Column('organisation_id', db.Integer(), db.ForeignKey('organisation.id'))
)
expertise_people = db.Table(
    'expertise_people',
    db.Column('person_id', db.Integer(), db.ForeignKey('person.id')),
    db.Column('expertise_id', db.Integer(), db.ForeignKey('expertise.id'))
)
projects_people = db.Table(
    'projects_people',
    db.Column('person_id', db.Integer(), db.ForeignKey('person.id')),
    db.Column('project_id', db.Integer(), db.ForeignKey('project.id'))
)
resources_people = db.Table(
    'resources_people',
    db.Column('person_id', db.Integer(), db.ForeignKey('person.id')),
    db.Column('resource_id', db.Integer(), db.ForeignKey('resource.id'))
)

class CareerStage(enum.Enum):
    UNDERGRAD = "Undergraduate student (e.g. BSc/BA)"
    POSTGRAD = "Postgraduate student (Masters/PhD student)"
    POSTDOC = "Postdoc/Junior Researcher"
    ACADEMIC = "Academic (Senior Researcher, Professor)"
    PUBLICSECTOR = "Practitioner in the public/government sector"
    PRIVATESECTOR = "Practitioner or business in the private sector"
    OTHER = "Other (short text)"

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orcid = db.Column(db.Unicode(128), unique=True, doc="ORCID is a persistent unique digital identifier that you own and control")
    source_id = db.Column(db.Unicode(64), unique=True)

    last_name = db.Column(db.Unicode(255))
    first_name = db.Column(db.Unicode(255))
    title = db.Column(db.Unicode(128))
    gender = db.Column(db.Unicode(64))
    position = db.Column(db.UnicodeText)
    #affiliation -> organisation
    contact_email = db.Column(db.Unicode(255))
    personal_urls = db.Column(db.UnicodeText)
    select_career_stage = db.Column(db.Unicode(64))
    career_stage_note = db.Column(db.Unicode(255))
    ecr_list = db.Column(db.Boolean(), doc="Would you like to be added to the ECR list of the MRI (applies for ECRs, <5 years from graduation)")
    official_functions = db.Column(db.UnicodeText)

    upload_photo = db.Column(db.String(512))

    allow_public = db.Column(db.Boolean(), doc="I allow publishing my profile on the web")
    allow_photo = db.Column(db.Boolean(), doc="I allow publishing my photo on the web")
    allow_contact = db.Column(db.Boolean(), doc="I allow MRI to contact me regarding my profile, as listed on the database, to link to and promote in its communications channels (website, social media, newsletter article).")
    allow_registry = db.Column(db.Boolean(), doc="I would like to be added to an experts registry for internal use by the MRI Coordination Office to identify and connect with external requests for consultancies, expertise, provide inputs for policy briefs/policy reviews, speaking role, or interviews (such as by thor parties, journalists or collaborators of the MRI).")
    allow_newsletter = db.Column(db.Boolean(), doc="I would like to receive monthly MRI Global Newsletters and Newsflashes from the MRI")

    def gravatar(self):
        gr_size = 80
        if self.email == "": return "/img/usericon.png"
        email = self.email.lower().encode('utf-8')
        gravatar_url = "https://www.gravatar.com/avatar/"
        gravatar_url += hashlib.md5(email).hexdigest() + "?"
        gravatar_url += urlencode({'s':str(gr_size)})
        return gravatar_url

    affiliation = db.relationship('Organisation', secondary=organisation_people,
        backref=db.backref('people', lazy='dynamic'))

    expertise = db.relationship('Expertise', secondary=expertise_people,
        backref=db.backref('people', lazy='dynamic'))

    projects = db.relationship('Project', secondary=projects_people,
        backref=db.backref('people', lazy='dynamic'))

    resources = db.relationship('Resource', secondary=resources_people,
        backref=db.backref('people', lazy='dynamic'))

    _indexer = db.Column(db.UnicodeText)
    def index(self):
        self._indexer = " ".join([
            self.first_name,
            self.last_name,
            self.position,
            # self.affiliation,
        ])
        return True

    @property
    def fullname(self):
        return " ".join([ self.title, self.first_name, self.last_name ])
    def __repr__(self):
        return self.fullname

    @property
    def career_stage(self):
        if self.select_career_stage == CareerStage.OTHER.name:
            return self.career_stage_note
        elif self.select_career_stage is not None:
            return CareerStage[self.select_career_stage].value
        return ''

    @property
    def urls(self):
        if not self.personal_urls: return []
        if ';' in self.personal_urls:
            return self.personal_urls.strip().split(';')
        else:
            return self.personal_urls.strip().split('\n')

    @property
    def thumbnail(self): return self.get_photo(True)

    @property
    def photo(self): return self.get_photo()

    def get_photo(self, as_thumbnail=False):
        if not self.upload_photo: return Config.DEFAULT_THUMB
        name, _ = ospath.splitext(self.upload_photo)
        if as_thumbnail:
            return '/uploads/' + secure_filename('%s_thumb.jpg' % name)
        return '/uploads/' + secure_filename('%s.jpg' % name)


class ResourceType(enum.Enum):
    HOMEPAGE = "Link to personal homepage"
    RESUME = "Link to online CV (e.g. LinkedIn)"
    PROFILE = "Link to profile (e.g. ResearchGate)"
    BOOK = "Publication (book)"
    PAPER = "Publication (journal paper)"
    ARTICLE = "Publication (online article)"

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(2048))
    url = db.Column(db.Unicode(2048))
    citation = db.Column(db.UnicodeText)
    abstract = db.Column(db.UnicodeText)
    resource_type = db.Column(db.Enum(ResourceType))

    def __repr__(self):
        return self.title

    @property
    def of_type(self):
        return self.resource_type.value

class ResourceView(ModelView):
    column_list = ('title', 'url')
    form_choices = {
        'resource_type': [(d.name, d.value) for d in ResourceType],
    }

class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # A short string describing this topic
    title = db.Column(db.Unicode(255))

    def __repr__(self):
        return self.title


class Expertise(db.Model):
    __tablename__ = "expertise"
    id = db.Column(db.Integer, primary_key=True)

    # Topics or sub-topics that this expertise belongs to
    topic_id = db.Column(db.Integer, db.ForeignKey(Topic.id))
    topic = db.relationship(Topic)

    # A short string with the name of this expertise
    # Presented as Multiple choice, e.g.:
    # Basic / Fundamental Research;
    # Applied Research / Technologies /
    # Engineering; Research Interface /
    # Management;
    # Interdisciplinary Research;
    # Transdisciplinary Research
    title = db.Column(db.Unicode(255))

    @property
    def json(self):
        return {
            'id':  self.id,
            'key': self.key,
            'filename': self.filename,
            'seq': self.sequence_key,
            'lat': self.latitude,
            'lon': self.longitude
        }

    def __repr__(self):
        return self.title


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # A short string describing this project
    name = db.Column(db.Unicode(255))
    acronym = db.Column(db.Unicode(16))
    date_start = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_end = db.Column(db.DateTime, default=db.func.current_timestamp())
    funding = db.Column(db.UnicodeText)
    investigators = db.Column(db.UnicodeText)
    homepage = db.Column(db.UnicodeText)
    location = db.Column(db.UnicodeText)

    def __repr__(self):
        return self.name


class Organisation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    # A short string describing this institution
    name = db.Column(db.Unicode(255))
    department = db.Column(db.Unicode(255))
    building = db.Column(db.UnicodeText)
    street = db.Column(db.UnicodeText)
    postcode = db.Column(db.Unicode(16))
    city = db.Column(db.Unicode(255))
    country = db.Column(db.Unicode(255))

    def __repr__(self):
        return self.name




class PersonView(ModelView):
    column_list = ('first_name', 'last_name', 'affiliation')
    form_choices = {
        'select_career_stage': [(d.name, d.value) for d in CareerStage],
        'resource_type': [(d.name, d.value) for d in ResourceType],
    }
    form_extra_fields = {
        'upload_photo': ImageUploadField('Photo',
            base_path=Config.UPLOAD_DIR,
            relative_path='photos/',
            endpoint='client_app.index_uploads',
            thumbnail_size=(256, 256, True))
    }
    inline_models = [Organisation, Expertise, Project, Resource]
