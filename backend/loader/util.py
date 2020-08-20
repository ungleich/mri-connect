
# Correct commas inside of a linked field
def fix_bracketed_lists(data):
    for fix in re.findall(r'\([^\s]*,[ ]*[^\s]*\)', data):
        data = data.replace(fix, fix.replace(',', ' /'))
    return data

# Check for valid link
def fix_url(link):
    if len(link) > 3 and not link.startswith('http'):
        link = 'http://' + link
    # link = link.split(';')[0]
    return link

# Create linked objects
def add_linked(person, field, obj, data):
    # TODO: fuzzy matching instead of lower()
    items = fix_bracketed_lists(data).lower()
    items = items.replace(';',',').split(',')
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

# Quick check of the number of lines
def get_total_rows_csv(filename):
    with open(filename) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

# Search index routine
def reindex_data():
    for i, p in enumerate(Person.query.all()):
        p.index()
        db.session.add(p)
        if i % 10 == 0: db.session.commit()
    db.session.commit()
