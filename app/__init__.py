from flask import Flask, Markup
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import flask_admin as admin
import click
import logging

# Create application
app = FlaskAPI(__name__)
from .config import Config
app.logger.info('>>> hi {}'.format(Config.FLASK_ENV))

gunicorn_logger = logging.getLogger('gunicorn.error')
if gunicorn_logger:
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

if Config.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
    app.logger.warn('Warning: SQLite database, changes may not persist.')
    app.logger.warn('>>> {}'.format(Config.SQLALCHEMY_DATABASE_URI))

db = SQLAlchemy(app)

from .models import *
migrate = Migrate(app, db)

# Create admin
adminlink = Config.ADMIN_PATH
app.logger.info('Admin access at /%s' % adminlink)
admin = admin.Admin(app, url='/'+adminlink, name='MRI Connect', template_mode='bootstrap3')

from .views import *
