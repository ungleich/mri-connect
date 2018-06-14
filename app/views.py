#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, admin
from .models import *
from flask_admin.contrib.sqla import ModelView, filters
from flask import (
    url_for,
    request,
    render_template,
    send_from_directory
)

import csv

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
def send_site(path):
    return send_from_directory('../client', path)
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('../client/static', path)

# Data update
@app.route('/refresh', methods=["POST"])
def refresh_data():
    count_p = 0
    with open('data/people_details.csv', 'rt') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if row is None: continue
            person = Person.query.filter_by(first_name=row['First name'], last_name=row['Last name']).first()
            if not person:  person = Person(first_name=row['First name'], last_name=row['Last name'])
            person.title = row['Title']
            person.organisation = row['Organisation English']
            person.country = row['Country']
            person.biography = row['Biography']
            person.contact_email = row['e-mail 1']
            person.personal_url = row['URL']

            db.session.add(person)
            count_p = count_p + 1
        db.session.commit()

    count_r = 0
    with open('data/resources.csv', 'rt') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if row is None: continue
            res = Resource.query.filter_by(title=row['Title']).first()
            if not res:     res = Resource(title=row['Title'])
            res.title = row['Title']
            res.citation = row['Citation']
            res.url = row['URL']
            res.abstract = row['Abstract']

            db.session.add(res)
            count_r = count_r + 1
        db.session.commit()

    return "%d people and %d resources updated<p><a href='/admin'>Continue</a>" % (count_p, count_r)
