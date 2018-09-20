from flask import Flask, Markup
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

import flask_admin as admin

# Create application
app = FlaskAPI(__name__, static_url_path='')
from .config import Config
app.logger.info('>>> {}'.format(Config.FLASK_ENV))

db = SQLAlchemy(app)

from .models import *
migrate = Migrate(app, db)


# Create admin
admin = admin.Admin(app, name='GMBA Connect', template_mode='bootstrap3')

from .views import *
