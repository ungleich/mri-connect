import csv, json, re
from os.path import isfile
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

# Fetch an object by source_id (numeric identifier used in source DB)
def get_by_id(rowid, obj, first=True):
    if type(rowid) is str and rowid.isdigit():
        rowid = int(rowid)
    if type(rowid) is int:
        l = obj.query.filter_by(source_id=rowid)
        if first: return l.first(), rowid
        else: return l, rowid
    return None, None

# Data update routine
def refresh_data(filename, fmt=None):
    count = 0
    if not isfile(filename):
        yield("Missing data: %s  - refresh aborted." % fmt['filename'], "error")
        return None
    if fmt['extension'] is 'csv':
        with open(filename, 'rt', encoding='utf-8', errors='ignore') as csvfile:
            datareader = csv.DictReader(csvfile)
            totalrows = 0
            for row in datareader: totalrows += 1
            csvfile.seek(0)

            for row in datareader:
                if row is None: continue

                yield count, count/totalrows
                # Ensure any new data is flushed
                db.session.commit()

                for r in fmt['required']:
                    if not r in row:
                        yield("Missing attribute in %s (%s)" % (r, fmt['filename']), "error")
                        return None

                if fmt['dataformat'] is DataFormat.PERSON_DETAIL:
                    person, source_id = get_by_id(row['ID'], Person)
                    if not person:
                        person = Person.query.filter_by(first_name=row['First name'], last_name=row['Last name']).first()
                    if not person:
                        person = Person(first_name=row['First name'], last_name=row['Last name'], source_id=row['ID'])

                    # Update data fields
                    person.source_id = source_id
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
                    res, source_id = get_by_id(row['ID'], Resource)
                    if not res: res = Resource(source_id=source_id)
                    res.title = row['Title']
                    res.citation = row['Citation']
                    res.url = row['URL']
                    res.abstract = row['Abstract']
                    db.session.add(res)
                    count = count + 1

                elif fmt['dataformat'] is DataFormat.RANGE_DETAIL:
                    rng, source_id = get_by_id(row['Range_ID'], Range)
                    if not rng: rng = Range(source_id=source_id)
                    rng.gmba_id = row['GMBA_ID']
                    rng.name = row['RangeName']
                    rng.countries = row['Countries']
                    db.session.add(rng)
                    count = count + 1

                elif fmt['dataformat'] is DataFormat.PERSON_RESOURCE:
                    rzs, source_id = get_by_id(row['Resource'], Resource, first=False)
                    if not rzs.first(): continue
                    ppl, source_id = get_by_id(row['Person'], Person, first=False)
                    if not ppl.first(): continue
                    for person in ppl:
                        for r in rzs: person.resources.append(r)
                        db.session.add(person)
                        count = count + 1

                elif fmt['dataformat'] is DataFormat.PERSON_RANGE:
                    rzs, source_id = get_by_id(row['MountainRange'], Range, first=False)
                    if not rzs.first(): continue
                    ppl, source_id = get_by_id(row['Person'], Person, first=False)
                    if not ppl.first(): continue
                    for person in ppl:
                        for r in rzs: person.ranges.append(r)
                        db.session.add(person)
                        count = count + 1

    elif fmt['extension'] is 'geojson':
        with open(filename, 'rt') as jsonfile:
            jsondata = json.load(jsonfile)
            if fmt['dataformat'] is DataFormat.RANGE_SHAPES:
                totalrows = len(jsondata['features'])
                for f in jsondata['features']:
                    yield count, count/totalrows
                    count = count + 1

                    p = f['properties']
                    rge = Range.query.filter_by(gmba_id=p['GMBA_ID']).first()
                    if not rge:
                        print("Range not found: %s" % p['GMBA_ID'])
                        continue
                    rge.name = p['Name']
                    for c in ['Country_1', 'Country_2_']:
                        if c in p: rge.countries = p[c]
                    db.session.add(rge)

    db.session.commit()
    whooshee.reindex()
    yield None, None
    return count

def reindex_search():
    whooshee.reindex()
