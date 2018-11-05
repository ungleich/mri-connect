#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db

resources_people = db.Table(
    'resources_people',
    db.Column('person_id', db.Integer(), db.ForeignKey('person.id')),
    db.Column('resource_id', db.Integer(), db.ForeignKey('resource.id'))
)
ranges_people = db.Table(
    'ranges_people',
    db.Column('person_id', db.Integer(), db.ForeignKey('person.id')),
    db.Column('range_id', db.Integer(), db.ForeignKey('range.id'))
)
methods_people = db.Table(
    'methods_people',
    db.Column('person_id', db.Integer(), db.ForeignKey('person.id')),
    db.Column('method_id', db.Integer(), db.ForeignKey('method.id'))
)
scales_people = db.Table(
    'scales_people',
    db.Column('person_id', db.Integer(), db.ForeignKey('person.id')),
    db.Column('scale_id', db.Integer(), db.ForeignKey('scale.id'))
)
taxa_people = db.Table(
    'taxa_people',
    db.Column('person_id', db.Integer(), db.ForeignKey('person.id')),
    db.Column('taxon_id', db.Integer(), db.ForeignKey('taxon.id'))
)
fields_people = db.Table(
    'fields_people',
    db.Column('person_id', db.Integer(), db.ForeignKey('person.id')),
    db.Column('field_id', db.Integer(), db.ForeignKey('field.id'))
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
    ranges = db.relationship('Range', secondary=ranges_people,
        backref=db.backref('people', lazy='dynamic'))

    research_methods = db.relationship('Method', secondary=methods_people,
        backref=db.backref('people', lazy='dynamic'))
    research_scales = db.relationship('Scale', secondary=scales_people,
        backref=db.backref('people', lazy='dynamic'))
    research_taxa = db.relationship('Taxon', secondary=taxa_people,
        backref=db.backref('people', lazy='dynamic'))
    research_fields = db.relationship('Field', secondary=fields_people,
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
    source_id = db.Column(db.Integer, unique=True)
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

class Range(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    source_id = db.Column(db.Integer, unique=True)
    gmba_id = db.Column(db.Unicode(32))
    name = db.Column(db.Unicode(255))
    countries = db.Column(db.Unicode(255))
    def __repr__(self):
        return self.name
    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'gmba_id': self.gmba_id,
            'countries': self.countries,
        }

class Method(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255))
    def __repr__(self): return self.name
    def dict(self):
        return { 'id': self.id, 'name': self.name, 'people': self.people }

class Scale(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255))
    def __repr__(self): return self.name
    def dict(self):
        return { 'id': self.id, 'name': self.name, 'people': self.people }

class Taxon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255))
    def __repr__(self): return self.name
    def dict(self):
        return { 'id': self.id, 'name': self.name, 'people': self.people }

class Field(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(255))
    def __repr__(self): return self.name
    def dict(self):
        return { 'id': self.id, 'name': self.name, 'people': self.people }
