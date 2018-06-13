#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, admin
from .models import *
from flask_admin.contrib.sqla import ModelView, filters

# Add views
admin.add_view(ModelView(Person, db.session))
admin.add_view(ModelView(Resource, db.session))

# API views
@app.route("/api/people", methods=['GET'])
def people_list():
    return [p.dict() for p in Person.query.limit(10).all()]

@app.route("/api/people/<int:people_id>", methods=['GET'])
def people_detail(people_id):
    person = Person.query.filter_by(id=people_id).first_or_404()
    return {
        'data': person.dict(),
        'resources': [r.dict() for r in person.resources]
    }

@app.route("/api/resources", methods=['GET'])
def resources_list():
    return [r.dict() for r in Resource.query.limit(10).all()]

# Static paths
@app.route('/site/<path:path>')
def send_static(path):
    return send_from_directory('../client/build', path)
