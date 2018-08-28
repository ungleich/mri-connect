from flask import Flask, Markup
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

import flask_admin as admin

# Create application
app = FlaskAPI(__name__, static_url_path='')
app.debug = True
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

# Create admin
admin = admin.Admin(app, name='GMBA Connect', template_mode='bootstrap3')

def init_app():
    db.create_all()
    print("Database initialized")
