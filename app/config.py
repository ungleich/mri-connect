"""
Global Flask Application Setting

set FLASK_CONFIG to 'development
 """

import os
from app import app
from tempfile import gettempdir

class Config(object):
    # If not set fall back to production for safety
    FLASK_ENV =  os.getenv('FLASK_ENV', 'production')
    # Set FLASK_SECRET on your production Environment
    SECRET_KEY = os.getenv('FLASK_SECRET', 'Secret')

    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)

    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'
    if 'SECRET_KEY' in os.environ:
        SECRET_KEY = os.environ['SECRET_KEY']

    # database connection
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    if 'DATABASE_URL' in os.environ:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    else:
        tf = os.path.join(gettempdir(), 'gmbaconnect.sqlite3')
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + tf

    # if not 'FLASK_ENV' is 'production':
    WHOOSHEE_MEMORY_STORAGE = True

    SERVER_URL = os.getenv('SERVER_URL', '')
    MAILGUN_DOMAIN = os.getenv('MAILGUN_DOMAIN', '')
    MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY', '')
    MAILGUN_TO = os.getenv('MAILGUN_TO', '').split(',')


app.config.from_object('app.config.Config')
