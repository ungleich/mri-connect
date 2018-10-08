from flask import Flask, Markup
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_whooshee import Whooshee
import flask_admin as admin

# Create application
app = FlaskAPI(__name__, static_url_path='')
from .config import Config
app.logger.info('>>> {}'.format(Config.FLASK_ENV))

if Config.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
    app.logger.info('Warning: temporary database, changes will not persist.')
    app.logger.info('>>> {}'.format(Config.SQLALCHEMY_DATABASE_URI))

db = SQLAlchemy(app)
whooshee = Whooshee(app)

from .models import *
migrate = Migrate(app, db)

# Create admin
admin = admin.Admin(app, name='GMBA Connect', template_mode='bootstrap3')

from .views import *

# Rebuild the search index on startup
whooshee.reindex()
