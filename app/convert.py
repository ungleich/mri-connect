import csv, json
from os.path import isfile
from flask import flash
from .models import *
from .formats import *

# Data update routine
def refresh_data(filename, fmt=None):
    count = 0
    if not isfile(filename):
        flash("Missing data: %s  - refresh aborted." % fmt['filename'])
        return None
    if fmt['extension'] is 'csv':
        with open(filename, 'rt') as csvfile:
            datareader = csv.DictReader(csvfile)
            for row in datareader:
                if row is None: continue

                for r in fmt['required']:
                    if not r in row:
                        flash("Missing attribute in %s (%s)" % (r, fmt['filename']))
                        return None

                if fmt['dataformat'] is DataFormat.PERSON_DETAIL:
                    person = Person.query.filter_by(first_name=row['First name'], last_name=row['Last name']).first()
                    if not person:
                        person = Person(first_name=row['First name'], last_name=row['Last name'])
                    person.source_id = row['ID']
                    person.title = row['Title']
                    person.organisation = row['Organisation English']
                    person.country = row['Country']
                    person.biography = row['Biography']
                    person.contact_email = row['e-mail 1']
                    person.personal_url = row['URL']
                    db.session.add(person)
                    count = count + 1

                elif fmt['dataformat'] is DataFormat.RESOURCE_DETAIL:
                    res = Resource.query.filter_by(title=row['Title']).first()
                    if not res:     res = Resource(title=row['Title'])
                    res.source_id = row['ID']
                    res.title = row['Title']
                    res.citation = row['Citation']
                    res.url = row['URL']
                    res.abstract = row['Abstract']
                    db.session.add(res)
                    count = count + 1

                elif fmt['dataformat'] is DataFormat.PERSON_RESOURCE:
                    rzs = Resource.query.filter_by(source_id=row['Resource'])
                    if not rzs.first(): continue
                    ppl = Person.query.filter_by(source_id=row['Person'])
                    if not ppl.first(): continue
                    for person in ppl:
                        for r in rzs: person.resources.append(r)
                        db.session.add(person)
                        count = count + 1

                elif fmt['dataformat'] is DataFormat.PERSON_RANGE:
                    rzs = Range.query.filter_by(source_id=row['MountainRange'])
                    if not rzs.first(): continue
                    ppl = Person.query.filter_by(source_id=row['Person'])
                    if not ppl.first(): continue
                    for person in ppl:
                        for r in rzs: person.ranges.append(r)
                        db.session.add(person)
                        count = count + 1

    elif fmt['extension'] is 'geojson':
        with open(filename, 'rt') as jsonfile:
            jsondata = json.load(jsonfile)
            if fmt['dataformat'] is DataFormat.RANGE_SHAPES:
                for f in jsondata['features']:
                    p = f['properties']
                    rge = Range.query.filter_by(gmba_id=p['GMBA_ID']).first()
                    if not rge:
                        #rge = Range(gmba_id=p['GMBA_ID'])
                        print("Range not found: %s" % p['GMBA_ID'])
                        continue
                    rge.name = p['Name']
                    for c in ['Country_1', 'Country_2_']:
                        if c in p: rge.countries = p[c]
                    db.session.add(rge)
                    count = count + 1

    db.session.commit()
    return count
