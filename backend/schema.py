# -*- coding: utf-8 -*-

from . import ma
from .models import (
    Person, Organisation, Expertise, Project, Resource
)
from marshmallow import fields, pre_load

class PersonSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Person
        fields = (
            'id',
            'last_name',
            'first_name',
            'fullname',
            'city',
            'country',
        )

class OrganisationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Organisation
        fields = (
            'name',
            'department',
            'building',
            'street',
            'postcode',
            'city',
            'country',
            'url',
        )


class ResourceSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Person
        fields = (
            'id',
            'title',
            'citation',
            'url',
            'abstract',
            'of_type',
        )


class PersonFullSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Person

    title = ma.auto_field()
    fullname = fields.Str()
    position = ma.auto_field()
    urls = fields.List(fields.Str())
    official_functions = fields.Str()
    career_stage = fields.Str()
    thumbnail = fields.Str()
    photo = fields.Str()

    affiliation = fields.List(fields.Nested(OrganisationSchema()))
    resources = fields.List(fields.Nested(ResourceSchema()))
