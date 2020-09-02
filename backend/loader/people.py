#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv

from .. import db
from ..models import Person, Organisation
from .util import *

def refresh_data(filename, required_cols=[]):
    totalrows = get_total_rows_csv(filename)
    count = 0

    with open(filename, 'rt', encoding='utf-8', errors='ignore') as csvfile:
        # dialect = csv.Sniffer().sniff(csvfile.read(2048), delimiters=";,")
        # csvfile.seek(0)
        datareader = csv.DictReader(csvfile, delimiter=";")
        rowcount = 0

        for row in datareader:

            rowcount += 1
            if row is None: continue
            yield rowcount, rowcount/totalrows

            # Ensure any new data is flushed from time to time
            if count % 25 == 0:
                db.session.commit()

            for r in required_cols:
                if not r in row:
                    msg = "Missing attribute in %s (%s)" % (r, fmt['filename'])
                    # app.logger.warn(msg)
                    yield(msg, "error")
                    return None

                person = Person.query.filter_by(
                    first_name=row['FirstN'],
                    last_name=row['Name']
                ).first()
                if not person:
                    org = None
                    if len(row['UniCompFull']) > 2:
                        org = Organisation.query.filter_by(
                            name =row['UniCompFull']
                        ).first()
                        if not org:
                            org = Organisation(
                                name    =row['UniCompFull'],
                                street  =row['Address2'],
                                city    =row['City'],
                                country =row['Country'],
                            )
                            db.session.add(org)

                    person = Person(
                        first_name =row['FirstN'],
                        last_name  =row['Name'],
                        title      =row['Title'],
                        source_id  =row['PersonID'],
                        position   =row['Position'],
                        gender     =row['Sex'],
                        # biography  =row['Info1'],
                        contact_email=row['Email'],
                        personal_urls=fix_url(row['URL_Person']),
                    )

                    if org is not None:
                        person.affiliation = [org]

                    db.session.add(person)
                    count = count + 1

    # Processing complete
    db.session.commit()
    return("%d people imported" % count)

def queue_refresh(filename, fmt):
    c = 1
    c_counter = 0
    rd = refresh_data(filename, fmt)
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
            print(str(c))
        elif isinstance(p, str) and isinstance(c, str):
            # Error condition
            print(p + ": " + c)
            return


def load_people(fn):
    msg = queue_refresh(
        fn,
        ["Name", "FirstN"],
    )
    if msg is not None:
        print(msg)
