#!/usr/bin/env python3
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.flaskenv')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from backend import create_app, db
from backend.models import *

app = create_app()


@app.cli.command()
def people():
    """ Import people database """
    from backend.loader.people import load_people
    with app.app_context():
        load_people()


if __name__ == '__main__':
    app.cli()
