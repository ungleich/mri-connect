import csv, json, re
from os.path import isfile
from flask import flash
from .models import *
from .formats import *

# Correct commas inside of a linked field
def fix_bracketed_lists(data):
    for fix in re.findall(r'\([^\s]*,[ ]*[^\s]*\)', data):
        data = data.replace(fix, fix.replace(',', ' /'))
    return data

# Create linked objects
def add_linked(person, field, obj, data):
    # TODO: fuzzy matching instead of lower()
    items = fix_bracketed_lists(data).lower().split(',')
    for i in items:
        n = i.strip()
        if len(n)<3: continue
        tgt = obj.query.filter_by(name=n).first()
        if not tgt:
            tgt = obj()
            tgt.name = n
        db.session.add(tgt)
        field.append(tgt)

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
                    person = Person.query.filter_by(source_id=row['ID']).first()
                    if not person:
                        person = Person.query.filter_by(first_name=row['First name'], last_name=row['Last name']).first()
                    if not person:
                        person = Person(first_name=row['First name'], last_name=row['Last name'], source_id=row['ID'])

                    # Update data fields
                    person.source_id = row['ID']
                    person.title = row['Title']
                    person.organisation = row['Organisation English']
                    person.country = row['Country']
                    person.position = row['Position']
                    person.biography = row['Biography']
                    person.contact_email = row['e-mail 1']
                    person.personal_url = row['URL']

                    with db.session.no_autoflush:
                        add_linked(person, person.research_methods, Method, row['Methods'])
                        add_linked(person, person.research_scales,  Scale,  row['Scale'])
                        add_linked(person, person.research_taxa,    Taxon,  row['Taxa'])
                        add_linked(person, person.research_fields,  Field,  row['Field of expertise'])

                    db.session.add(person)
                    count = count + 1

                elif fmt['dataformat'] is DataFormat.RESOURCE_DETAIL:
                    res = Resource.query.filter_by(source_id=row['ID']).first()
                    if not res:     res = Resource(source_id=row['ID'])
                    res.title = row['Title']
                    res.citation = row['Citation']
                    res.url = row['URL']
                    res.abstract = row['Abstract']
                    db.session.add(res)
                    count = count + 1

                elif fmt['dataformat'] is DataFormat.RANGE_DETAIL:
                    rng = Range.query.filter_by(source_id=row['Range_ID']).first()
                    if not rng: rng = Range(source_id=row['Range_ID'])
                    rng.gmba_id = row['GMBA_ID']
                    rng.name = row['RangeName']
                    rng.countries = row['Countries']
                    db.session.add(rng)
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
                        print("Range not found: %s" % p['GMBA_ID'])
                        continue
                    rge.name = p['Name']
                    for c in ['Country_1', 'Country_2_']:
                        if c in p: rge.countries = p[c]
                    db.session.add(rge)
                    count = count + 1

    db.session.commit()
    whooshee.reindex()
    return count

def reindex_search():
    whooshee.reindex()
