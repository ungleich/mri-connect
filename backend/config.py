"""
Global Flask Application Settings
"""

import os
from tempfile import gettempdir

class Config(object):
    # If not set fall back to production for safety
    FLASK_ENV =  os.getenv('FLASK_ENV', 'production')
    # Set FLASK_SECRET on your production Environment
    SECRET_KEY = os.getenv('FLASK_SECRET', 'Secret')

    APP_DIR = os.path.dirname(__file__)
    ROOT_DIR = os.path.dirname(APP_DIR)
    DIST_DIR = os.path.join(ROOT_DIR, 'dist')
    UPLOAD_DIR = os.path.join(ROOT_DIR, 'uploads')
    DEFAULT_THUMB = '/images/avatar.jpg'

    SSL_REDIRECT = os.getenv('SSL_REDIRECT', False)

    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'
    if 'SECRET_KEY' in os.environ:
        SECRET_KEY = os.environ['SECRET_KEY']

    # database connection
    SQLALCHEMY_ECHO = False #(FLASK_ENV == 'development')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    if 'DATABASE_URL' in os.environ:
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    else:
        tf = os.path.join(gettempdir(), 'connect.sqlite3')
        SQLALCHEMY_DATABASE_URI = 'sqlite:///' + tf

    # Location of admin interface
    ADMIN_PATH = os.getenv('ADMIN_PATH', 'admin')
    FLASK_ADMIN_SWATCH = 'cerulean'
