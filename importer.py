#!/usr/bin/env python3
import os, click
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from backend import create_app, db
from backend.models import *

app = create_app()


@app.cli.command()
@click.argument('filename')
def people(filename):
    """ Import people database """
    from backend.loader.people import load_people
    from backend.loader.util import reindex_data
    with app.app_context():
        load_people(filename)
        reindex_data(db, Person)


if __name__ == '__main__':
    app.cli()
