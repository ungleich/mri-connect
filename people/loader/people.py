#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

from pprint import pprint
from django_countries import countries
from django.core.exceptions import ValidationError

from rapidfuzz import fuzz

from ..models import Person, Affiliation, Expertise, Topic
from .util import *

# TODO: -> config or option
errfilename = 'import.log'
expertisematchfile = 'convert/proclim_expertise.csv'

def fuzzymatch(what, o1, o2, min=90, warn=99):
    matcher = fuzz.ratio(o1.lower(), o2.lower())
    if matcher > min:
        if matcher < warn:
            print("Warning: %s [%s] uncertain match to [%s] %d" % (what, o1, o2, matcher))
        return True
    return False

def add_person(row, m_top, m_exp):
    # Validate email
    EMailAddress = row['EMailAddress'] or row['EMailAddress2'] or ''
    EMailAddress = EMailAddress.strip()
    if not '@' in EMailAddress:
        return '%s;%s;;%s;No e-mail' % (row['Name'], row['FirstName'], row['PersonID'])
    try:
        Person.objects.get(
            contact_email=EMailAddress
        )
        return ';;%s;Duplicate e-mail' % EMailAddress
    except Person.DoesNotExist:
        pass

    # Validate name
    FullName = row['FirstName'] or row['Name']
    if FullName is None or not len(FullName.strip())>2:
        return ';;%s;%s;No name' % (EMailAddress, row['PersonID'])
    try:
        Person.objects.get(
            first_name=row['FirstName'],
            last_name=row['Name']
        )
        return '%s;%s;;%s;Duplicate name' % (row['Name'], row['FirstName'], row['PersonID'])
    except Person.DoesNotExist:
        pass

    # Import person object
    try:
        person = Person(
            first_name   =row['FirstName'].strip(),
            last_name    =row['Name'].strip(),
            title        =row['Title'].strip(),
            proclimid    =row['PersonID'],
            position     =row['PPosition'].strip(),
            gender       =row['Sex'].strip().upper(),
            contact_email=EMailAddress,
            url_personal =fix_url(row['URL_site']).strip(),
            url_cv       =fix_url(row['URL_CurrVitae']).strip(),
            list_publications=fix_pub(row['KeyPublications']),
        )
        person.full_clean()
        person.save(force_insert=True)
    except ValidationError as e:
        return ';;%s;%s;%s' % (EMailAddress, row['PersonID'], repr(e))

    # Match institution
    org_name = row['UnivCompAbbr'].strip()
    org_country = row['CountryName'].strip()
    if len(org_name) > 2:
        org = None
        try:
            for a in Affiliation.objects.filter(name=org_name).all():
                if fuzzymatch('country seek', a.country.name, org_country):
                    org = a
                    break
            if org is None:
                raise Affiliation.DoesNotExist
        except Affiliation.DoesNotExist:
            org = Affiliation(
                name     =org_name,
                street   =row['Street'],
                post_code=row['ZIPCode'],
                city     =row['City'],
            )
            for code, name in list(countries):
                if fuzzymatch('country add', name, row['CountryName']):
                    org.country = code
                    break
            org.save()
        if org is not None:
            person.affiliation = org

    for exp in row['Expertise'].split(';'):
        exp = exp.strip()

        # Match expertise
        for old_exp in m_exp:
            if fuzzymatch('expertise', exp, old_exp, warn=93):
                for new_exp in m_exp[old_exp]:
                    expertise = Expertise.objects.get(
                        title = new_exp
                    )
                    person.expertise.add(expertise)
                break

    person.save()
    return True


def load_expertise_match(filename, delimiter=','):
    matcher_topic = {}
    matcher_exper = {}

    with open(filename, 'rt', encoding='utf-8', errors='ignore') as csvfile:
        datareader = csv.DictReader(csvfile, delimiter=delimiter)
        rowcount = 0

        for row in datareader:
            row_exper = row['Expertise'].strip().strip(';')
            row_topic = row['Topic'].strip()

            try:
                expertise = Expertise.objects.get(
                    title = row_exper
                )
            except Expertise.DoesNotExist:
                topic = None
                if row_topic:
                    try:
                        topic = Topic.objects.get(
                            title = row_topic
                        )
                    except Topic.DoesNotExist:
                        topic = Topic(
                            title = row_topic
                        )
                        topic.save()
                # Add expertise
                expertise = Expertise(
                    title = row_exper,
                    topic = topic
                )
                expertise.save()

            old_class = row['Old_Class'].replace('Topic','').strip().strip(';')

            if old_class == '':
                pass
            elif not old_class in matcher_topic:
                matcher_topic[old_class] = row_topic
            elif row_topic != matcher_topic[old_class]:
                print("Warning: class [%s] is ambiguous: [%s] vs [%s]" % (old_class, row_topic, matcher_topic[old_class]))

            old_expers = row['Old_Expertise'].split('/')

            for e in old_expers:
                old = e.strip().strip(';')
                if '' == old: continue

                if not old in matcher_exper:
                    matcher_exper[old] = []
                if not row_exper in matcher_exper[old]:
                    matcher_exper[old].append(row_exper)
                else:
                    print("Warning: expertise [%s] is ambiguous" % row_exper)

    return matcher_topic, matcher_exper


def refresh_data(filename, required_cols, delimiter, m_top, m_exp):
    totalrows = get_total_rows_csv(filename)
    count = 0

    with open(errfilename, 'w', encoding='utf-8', errors='ignore') as errorfile:
        errorfile.write('Name;FirstName;EMailAddress;PersonID;Message\n')
        with open(filename, 'rt', encoding='utf-8', errors='ignore') as csvfile:
            # dialect = csv.Sniffer().sniff(csvfile.read(2048), delimiters=";,")
            # csvfile.seek(0)
            datareader = csv.DictReader(csvfile, delimiter=delimiter)
            rowcount = 0

            for row in datareader:

                rowcount += 1
                if row is None: continue
                yield rowcount, rowcount/totalrows

                for r in required_cols:
                    if not r in row:
                        msg = "Missing attribute %s in schema." % r
                        # app.logger.warn(msg)
                        yield(msg, "error")
                        return None

                result = add_person(row, m_top, m_exp)
                if result == True:
                    count = count + 1
                elif type(result) == str:
                    # Skipping this person
                    errorfile.write(result + '\n')

    print("%d rows processed" % rowcount)
    print("%d people imported" % count)
    yield None, None

def queue_refresh(filename, required_cols=[], delimiter=";"):
    m_top, m_exp = load_expertise_match(expertisematchfile)
    print("Class - Topic mapping")
    print("---------------------")
    pprint(m_top)
    print("Old-new Expertise mapping")
    print("-------------------------")
    pprint(m_exp)
    print("-------------------------")
    c = 1
    c_counter = 0
    print("Starting import ...")
    print("-------------------")
    rd = refresh_data(filename, required_cols, delimiter, m_top, m_exp)
    while c is not None:
        c, p = next(rd)
        if isinstance(c, (int, float)):
            global c_progress
            c_counter = c
            if isinstance(p, (int, float)):
                c_progress = p
            if int(c) % 100 == 0:
                # Print message every N lines
                print(str(c))
        elif isinstance(p, str) and isinstance(c, str):
            # Error condition
            print(p + ": " + c)
            return
