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
            'title',
            'gender',
            'position',
            'urls',
            'fullname',
            'career_stage',
            'thumbnail',
            'photo',
        )


class OrganisationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Organisation

    name = ma.auto_field()
    department = ma.auto_field()
    building = ma.auto_field()
    street = ma.auto_field()
    postcode = ma.auto_field()
    city = ma.auto_field()
    country = ma.auto_field()


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
