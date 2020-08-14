from flask import Flask, Markup
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

import click
import logging

# TODO: track solution to https://github.com/jarus/flask-testing/issues/143
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property

db = SQLAlchemy()
migrate = Migrate()

from .config import Config

def create_app():
    app = Flask(__name__, static_folder='../dist/static')
    app.config.from_object('backend.config.Config')
    app.logger.info('>>> {}'.format(Config.FLASK_ENV))

    gunicorn_logger = logging.getLogger('gunicorn.error')
    if gunicorn_logger:
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    if Config.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
        app.logger.warn('Warning: SQLite database, changes may not persist.')
        app.logger.warn('>>> {}'.format(Config.SQLALCHEMY_DATABASE_URI))


    # Set up the database
    db.init_app(app)
    from .models import (
        Person, PersonView,
        Resource, ResourceView,
        Topic,
        Expertise,
        Project,
        Organisation,
    )
    migrate.init_app(app, db)


    # Register blueprints
    from .client import client_bp
    app.register_blueprint(client_bp)

    from .api import api_bp
    app.register_blueprint(api_bp)


    # Create admin
    adminlink = Config.ADMIN_PATH
    admin = Admin(app, url='/'+adminlink, name='MRI Connect', template_mode='bootstrap3')
    app.logger.info('Admin access at /%s' % adminlink)

    admin.add_view(PersonView(Person, db.session))
    admin.add_view(ModelView(Expertise, db.session))
    admin.add_view(ModelView(Organisation, db.session))
    admin.add_view(ModelView(Project, db.session))
    admin.add_view(ResourceView(Resource, db.session))

    return app
