from os import environ

SECRET_KEY = environ.get('SECRET_KEY', 'PLZ_CHANGE_ME')
SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL', 'sqlite:///gmba.sqlite3')
SQLALCHEMY_TRACK_MODIFICATIONS = False
if environ.get('DEBUG'):
    SQLALCHEMY_ECHO = True
