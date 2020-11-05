#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
from django_countries import countries
from rapidfuzz import fuzz

from ..models import Person, Affiliation
from .util import *

def add_person(row):
    try:
        person = Person.objects.get(
            first_name=row['FirstName'],
            last_name=row['Name']
        )
        return False
    except Person.DoesNotExist:
        pass
    try:
        person = Person.objects.get(
            contact_email=row['EMailAddress'] or row['EMailAddress2']
        )
        return False
    except Person.DoesNotExist:
        pass

    org = None
    if len(row['UnivCompAbbr']) > 2:
        org_name = row['UnivCompAbbr'].strip()
        try:
            org = Affiliation.objects.get(
                name= org_name
            )
        except Affiliation.DoesNotExist:
            org = Affiliation(
                name     =org_name,
                street   =row['Street'],
                post_code=row['ZIPCode'],
                city     =row['City'],
            )
            for code, name in list(countries):
                if fuzz.ratio(name.lower(), row['CountryName'].lower()) > 90:
                    org.country = code
            org.save()

    person = Person(
        first_name   =row['FirstName'],
        last_name    =row['Name'],
        title        =row['Title'],
        proclimid    =row['PersonID'],
        position     =row['PPosition'],
        gender       =row['Sex'],
        contact_email=row['EMailAddress'] or row['EMailAddress2'],
        url_personal =fix_url(row['URL_site']),
        url_cv       =fix_url(row['URL_CurrVitae']),
    )

    if org is not None:
        person.affiliation = org

    person.save()
    return True

def refresh_data(filename, required_cols, delimiter):
    totalrows = get_total_rows_csv(filename)
    count = 0

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

            if add_person(row):
                count = count + 1
            else:
                # Skipping this person
                pass

    return("%d people imported" % count)

def queue_refresh(filename, required_cols=[], delimiter=";"):
    c = 1
    c_counter = 0
    print("Starting import ...")
    rd = refresh_data(filename, required_cols, delimiter)
    while c is not None:
        try:
            c, p = next(rd)
        except Exception as e:
            print(str(e))
            return
        if isinstance(c, (int, float)):
            global c_progress
            c_counter = c
            if isinstance(p, (int, float)):
                c_progress = p
            if int(c) % 10 == 0:
                # Print message every N lines
                print(str(c))
        elif isinstance(p, str) and isinstance(c, str):
            # Error condition
            print(p + ": " + c)
            return
