import os

SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'
if 'SECRET_KEY' in os.environ:
    SECRET_KEY = os.environ['SECRET_KEY']

# database connection
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///gmba.sqlite3'

if 'DATABASE_URL' in os.environ:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
