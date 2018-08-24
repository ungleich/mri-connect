#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app, db, admin
from .models import *
from .formats import *

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

import csv, json
import os.path as ospath
from shutil import move
from tempfile import gettempdir

# Get temporary file storage
UPLOAD_PATH = gettempdir()
DATA_PATH = ospath.join(ospath.dirname(__file__), '..', 'data')

# Add views
class PersonView(ModelView):
    column_list = ('first_name', 'last_name', 'organisation')
admin.add_view(PersonView(Person, db.session))

class ResourceView(ModelView):
    column_list = ('title', 'citation', 'url')
admin.add_view(ResourceView(Resource, db.session))

class RangeView(ModelView):
    column_list = ('name', 'countries')
admin.add_view(RangeView(Range, db.session))

# Custom view
class ConfigurationView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/config.html', DATAFORMATS=DATAFORMATS)

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

@app.route("/api/ranges", methods=['GET'])
def ranges_list():
    return [r.dict() for r in Range.query.limit(10).all()]

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
        fmt = None
        if fs_name.endswith('.csv'):
            with open(fs_path, 'rt') as csvfile:
                datareader = csv.DictReader(csvfile)
                fmt = detect_dataformat(datareader)
                if fmt is not None:
                    count = length(datareader)

        elif fs_name.endswith('.geojson'):
            with open(fs_path, 'rt') as jsonfile:
                jsondata = json.load(jsonfile)
                fmt = detect_dataformat(jsondata['features'][0]['properties'])
                if fmt is not None:
                    count = length(jsondata['features'])

        # Loading
        if count > 0 and fmt is not None:
            fs_target = ospath.join(DATA_PATH, fmt['filename'], fmt['extension'])
            move(fs_path, fs_target)
            flash("Uploaded, validated and imported %d objects for " %
                (count, fmt['filename']))
            return refresh_data(fmt)
        else:
            flash("Could not detect data format!")
    else:
        flash("Please select a valid file")
    return redirect(url_for('config.index'))

# Data update routine
def refresh_data(fmt=None):
    count = 0
    filename = ospath.join(DATA_PATH, fmt['filename'] + '.' + fmt['extension'])
    if not ospath.isfile(filename): return None
    if fmt['extension'] is 'csv':
        with open(filename, 'rt') as csvfile:
            datareader = csv.DictReader(csvfile)
            for row in datareader:
                if row is None: continue

                if fmt is DataFormat.PERSON_DETAIL:
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
                    count = count + 1

                elif fmt is DataFormat.RESOURCE_DETAIL:
                    res = Resource.query.filter_by(title=row['Title']).first()
                    if not res:     res = Resource(title=row['Title'])
                    res.source_id = row['Id']
                    res.title = row['Title']
                    res.citation = row['Citation']
                    res.url = row['URL']
                    res.abstract = row['Abstract']
                    db.session.add(res)
                    count = count + 1

                elif fmt is DataFormat.PERSON_RESOURCE:
                    rzs = Resource.query.filter_by(source_id=row['Resource'])
                    if not rzs.first(): continue
                    ppl = Person.query.filter_by(source_id=row['Person'])
                    if not ppl.first(): continue
                    for person in ppl:
                        for r in rzs: person.resources.add(r)
                        db.session.add(person)
                        count = count + 1

                elif fmt is DataFormat.PERSON_RANGE:
                    rzs = Range.query.filter_by(source_id=row['MountainRange'])
                    if not rzs.first(): continue
                    ppl = Person.query.filter_by(source_id=row['Person'])
                    if not ppl.first(): continue
                    for person in ppl:
                        for r in rzs: person.ranges.add(r)
                        db.session.add(person)
                        count = count + 1

    elif fmt['extension'] is 'geojson':
        with open(filename, 'rt') as jsonfile:
            jsondata = json.load(jsonfile)
            if fmt is DataFormat.RANGE_SHAPES:
                for f in jsondata['features']:
                    p = f['properties']
                    rge = Range.query.filter_by(gmbaid=p['GMBA_ID']).first()
                    if not rge: rge = Range(gmbaid=p['GMBA_ID'])
                    rge.name = p['Name']
                    rge.countries = p['Country_2_']
                    db.session.add(rge)
                    count = count + 1

    db.session.commit()
    return count

# Data update
@app.route('/refresh', methods=["POST"])
def refresh_all():
    stats = []
    count_total = 0
    for fmt in DATAFORMATS:
        count = refresh_data(fmt)
        if count is None:
            flash("Missing data: %s (refresh aborted)" % fmt['filename'])
            return redirect(url_for('config.index'))
        stats.append({ 'format': fmt['dataformat'], 'count': count })
        count_total = count_total + count
    flash("%d objects updated" % (count_total))
    print(stats)
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
