# -*- coding: utf-8 -*-

from . import db, Config
from flask_admin.contrib.sqla import ModelView

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


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Unicode(64), unique=True)
    last_name = db.Column(db.Unicode(255))
    first_name = db.Column(db.Unicode(255))
    title = db.Column(db.Unicode(128))
    gender = db.Column(db.Unicode(64))
    position = db.Column(db.UnicodeText)
    contact_email = db.Column(db.Unicode(255))
    personal_urls = db.Column(db.UnicodeText)
    biography = db.Column(db.UnicodeText)

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
            self.first_name, self.last_name, self.affiliation, self.position, self.biography
        ])
        return True

    def fullname(self):
        return " ".join([ self.title, self.first_name, self.last_name ])
    def __repr__(self):
        return self.fullname()

    def dict(self):
        return {
            'id': self.id,
            'fullname': self.fullname(),
            'position': self.position or '',
            'personal_urls': (self.personal_urls or '').split(';'),
            'biography': self.biography or '',
        }

class PersonView(ModelView):
    column_list = ('first_name', 'last_name', 'affiliation')


class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Unicode(2048), unique=True)
    title = db.Column(db.Unicode(2048))
    url = db.Column(db.Unicode(2048))
    citation = db.Column(db.UnicodeText)
    abstract = db.Column(db.UnicodeText)

    def __repr__(self):
        return self.title
    def dict(self):
        return {
            'id': self.id,
            'source_id': self.source_id,
            'title': self.title or '',
            'citation': self.citation or '',
            'url': self.url or '',
            'abstract': self.abstract or '',
        }

class ResourceView(ModelView):
    column_list = ('title', 'url')


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
    official_functions = db.Column(db.UnicodeText)

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
    building = db.Column(db.UnicodeText)
    street = db.Column(db.UnicodeText)
    postcode = db.Column(db.Unicode(16))
    city = db.Column(db.Unicode(255))
    country = db.Column(db.Unicode(255))

    def __repr__(self):
        return self.name
