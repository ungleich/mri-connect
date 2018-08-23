#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, admin
from .models import *
from flask_admin.contrib.sqla import ModelView, filters
from flask_admin.form import FileUploadField
from flask_admin import (
    BaseView, expose
)
from flask import (
    url_for, redirect,
    request, flash,
    render_template,
    send_from_directory,
)
from werkzeug import secure_filename

import csv
import os.path as ospath
from shutil import move
from tempfile import gettempdir

# Get temporary file storage
UPLOAD_PATH = gettempdir()
DATAFILE = ospath.join(ospath.dirname(__file__), '..', 'data', 'people_details.csv')

# Add views
class PersonView(ModelView):
    column_list = ('first_name', 'last_name', 'organisation')
admin.add_view(PersonView(Person, db.session))

class ResourceView(ModelView):
    column_list = ('title', 'citation', 'url')
admin.add_view(ResourceView(Resource, db.session))

# Custom view
class ConfigurationView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/config.html')

admin.add_view(ConfigurationView(name='Configuration', endpoint='config'))

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

# Data upload
@app.route('/upload', methods=['GET', 'POST'])
def upload_data():
    if request.method == 'POST' and 'datafile' in request.files:
        fs = request.files['datafile']
        fs_name = secure_filename(fs.filename)
        fs_path = ospath.join(UPLOAD_PATH, fs_name)
        fs.save(fs_path)
        # Validation
        count = 0
        with open(fs_path, 'rt') as csvfile:
            datareader = csv.DictReader(csvfile)
            for row in datareader:
                if row is None: continue
                person = Person(first_name=row['First name'], last_name=row['Last name'])
                person.title = row['Title']
                person.organisation = row['Organisation English']
                person.country = row['Country']
                person.biography = row['Biography']
                person.contact_email = row['e-mail 1']
                person.personal_url = row['URL']
                count = count + 1
        if count > 0:
            move(fs_path, DATAFILE)
        flash("Uploaded and validated %d rows" % count)
        return refresh_data()
    else:
        flash("Please select a valid file")
    return redirect(url_for('config.index'))

# Data update
@app.route('/refresh', methods=["POST"])
def refresh_data():
    if not ospath.isfile(DATAFILE):
        flash("Add people_details, resources CSV files to the data folder first.")
        return redirect(url_for('admin.index'))

    count_p = 0
    with open(DATAFILE, 'rt') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            if row is None: continue
            person = Person.query.filter_by(first_name=row['First name'], last_name=row['Last name']).first()
            if not person:
                person = Person(first_name=row['First name'], last_name=row['Last name'])
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

    flash("%d people and %d resources updated from dataset" % (count_p, count_r))
    return redirect(url_for('config.index'))

# Static paths
@app.route('/data/<path:path>')
def send_data(path):
    return send_from_directory('../data', path)
@app.route('/client/<path:path>')
def send_client(path):
    return send_from_directory('../client', path)
@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('../static', path)
