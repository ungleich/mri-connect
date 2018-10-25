from flask import Flask, Markup
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_whooshee import Whooshee
import flask_admin as admin
import click

# Create application
app = FlaskAPI(__name__, static_url_path='')
from .config import Config
app.logger.info('>>> {}'.format(Config.FLASK_ENV))

if Config.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
    app.logger.info('Warning: temporary database, changes will not persist.')
    app.logger.info('>>> {}'.format(Config.SQLALCHEMY_DATABASE_URI))

db = SQLAlchemy(app)
whooshee = Whooshee(app)
try:
    whooshee.reindex()
    app.logger.info('Search engine index ready.')
except Exception:
    app.logger.warn('Could not reindex search, is the database migrated?')

from .models import *
migrate = Migrate(app, db)

# Create admin
try:
    import uuid, requests
    hashlink = str(uuid.uuid1())
    if Config.MAILGUN_DOMAIN is not '':
        requests.post(
            "https://api.mailgun.net/v3/%s/messages" % Config.MAILGUN_DOMAIN,
            auth=("api", Config.MAILGUN_API_KEY),
            data={"to": Config.MAILGUN_TO,
                  "from": "GMBA Connect <noreply@datalets.ch>",
                  "subject": "System Notification",
                  "text": "The admin interface is ready at %s/%s" %
                    (Config.SERVER_URL, hashlink)})
except Exception as ex:
    hashlink = 'default-admin'
    app.logger.warn(ex)
app.logger.info('Admin access at /%s' % hashlink)
admin = admin.Admin(app, url='/'+hashlink, name='GMBA Connect', template_mode='bootstrap3')

from .views import *
