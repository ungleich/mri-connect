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
from enum import Enum

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

class DataFormat(Enum):
    PERSON_DETAIL = 1
    PERSON_RESOURCE = 2
    PERSON_RANGE = 3
    RESOURCE_DETAIL = 4

def detect_dataformat(datareader):
    if datareader.length == 0: return None
    row = datareader[0]
    if 'First name' in row and 'Biography' in row:
        return DataFormat.PERSON_DETAIL
    if 'Citation' in row and 'Abstract' in row:
        return DataFormat.RESOURCE_DETAIL
    if 'Resource' in row and 'Person' in row:
        return DataFormat.PERSON_RESOURCE
    if 'Person' in row and 'MountainRange' in row:
        return DataFormat.PERSON_RANGE

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
            if detect_dataformat(datareader) is None:
                flash("Could not detect data format!")
            else:
                for row in datareader:
                    if row is None: continue
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
        datafmt = detect_dataformat(datareader)
        if datafmt is DataFormat.PERSON_DETAIL:
            for row in datareader:
                if row is None: continue
                person = Person.query.filter_by(first_name=row['First name'], last_name=row['Last name']).first()
                if not person:
                    person = Person(first_name=row['First name'], last_name=row['Last name'])
                person.source_id = row['Id']
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
        if datafmt is DataFormat.RESOURCE_DETAIL:
            for row in datareader:
                if row is None: continue
                res = Resource.query.filter_by(title=row['Title']).first()
                if not res:     res = Resource(title=row['Title'])
                res.source_id = row['Id']
                res.title = row['Title']
                res.citation = row['Citation']
                res.url = row['URL']
                res.abstract = row['Abstract']

                db.session.add(res)
                count_r = count_r + 1
        db.session.commit()

    count_rp = 0
    with open('data/people_resources.csv', 'rt') as csvfile:
        datareader = csv.DictReader(csvfile)
        if datafmt is DataFormat.PERSON_RESOURCE:
            for row in datareader:
                if row is None: continue
                rzs = Resource.query.filter_by(source_id=row['Resource'])
                if not rzs.first(): continue
                ppl = Person.query.filter_by(source_id=row['Person'])
                if not ppl.first(): continue
                for person in ppl:
                    for resource in rzs:
                        person.resources.add(rzs)
                        db.session.add(person)
                count_rp = count_rp + 1
        db.session.commit()

    flash("%d people, %d resources, %d links updated from dataset" % (count_p, count_r, count_rp))
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
