import os
from .base import *

env = os.environ.copy()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATES[0]['OPTIONS']['debug'] = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'CHANGEME!!!'

# SECURITY WARNING: CAREFUL! your dev site is open to the world
ALLOWED_HOSTS = ['*']

INTERNAL_IPS = ('127.0.0.1', '10.0.2.2')

BASE_URL = 'http://localhost:8000'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

INSTALLED_APPS = INSTALLED_APPS + [
    'debug_toolbar'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': env.get('PGDATABASE', 'app'),
        'CONN_MAX_AGE': 600,  # number of seconds database connections should persist for
        'USER': 'app'
        # User, host and port can be configured by the PGUSER, PGHOST and
        # PGPORT environment variables (these get picked up by libpq).
    }
}

MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + MIDDLEWARE

try:
    from .local import *
except ImportError:
    pass
