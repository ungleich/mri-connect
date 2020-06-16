#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db

resources_people = db.Table(
    'resources_people',
    db.Column('person_id', db.Integer(), db.ForeignKey('person.id')),
    db.Column('resource_id', db.Integer(), db.ForeignKey('resource.id'))
)

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, unique=True)
    title = db.Column(db.Unicode(128))
    first_name = db.Column(db.Unicode(255))
    last_name = db.Column(db.Unicode(255))
    organisation = db.Column(db.Unicode(512))
    position = db.Column(db.Unicode(512))
    country = db.Column(db.Unicode(512))
    contact_email = db.Column(db.Unicode(255))
    personal_url = db.Column(db.Unicode(2048))
    biography = db.Column(db.UnicodeText)

    resources = db.relationship('Resource', secondary=resources_people,
        backref=db.backref('people', lazy='dynamic'))

    _indexer = db.Column(db.UnicodeText)
    def index(self):
        self._indexer = " ".join([
            self.first_name, self.last_name, self.organisation, self.position, self.biography
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
            'organisation': self.organisation or '',
            'position': self.position or '',
            'country': self.country or '',
            'personal_url': self.personal_url or '',
            'personal_urls': self.personal_url.split(';'),
            'biography': self.biography or '',
        }

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    orcid = db.Column(db.Integer, unique=True)
    title = db.Column(db.Unicode(2048))
    url = db.Column(db.Unicode(2048))
    citation = db.Column(db.UnicodeText)
    abstract = db.Column(db.UnicodeText)
    def __repr__(self):
        return self.title
    def dict(self):
        return {
            'id': self.id,
            'title': self.title or '',
            'citation': self.citation or '',
            'url': self.url or '',
            'abstract': self.abstract or '',
        }


# class Topic(db.Model):
#     # A short string describing this topic
#     title = db.Column(db.String(100))
#
#     def __repr__(self):
#         return self.title

class Expertise(db.Model):
    __tablename__ = "expertise"
    id = db.Column(db.Integer, primary_key=True)

    # Topics or sub-topics that this expertise belongs to
    # topic_id = db.Column(db.Integer, db.ForeignKey(Topic.id))
    # topic = db.relationship(Topic)

    # A short string with the name of this expertise
    # Presented as Multiple choice, e.g.:
    # Basic / Fundamental Research;
    # Applied Research / Technologies /
    # Engineering; Research Interface /
    # Management;
    # Interdisciplinary Research;
    # Transdisciplinary Research
    title = db.Column(db.String(100))
    official_functions = db.Column(db.Text)

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
