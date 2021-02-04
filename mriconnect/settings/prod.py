import os
import dj_database_url

from .base import *

# Do not set SECRET_KEY, Postgres or LDAP password or any other sensitive data here.
# Instead, use environment variables or create a local.py file on the server.

# Disable debug mode
DEBUG = False
TEMPLATES[0]['OPTIONS']['debug'] = False

# Configuration from environment variables
# Alternatively, you can set these in a local.py file on the server
env = os.environ.copy()

# Basic configuration
APP_NAME = env.get('APP_NAME', 'mriconnect')

if 'SECRET_KEY' in env:
    SECRET_KEY = env['SECRET_KEY']

if 'ALLOWED_HOSTS' in env:
    ALLOWED_HOSTS = env['ALLOWED_HOSTS'].split(',')

if 'PRIMARY_HOST' in env:
    BASE_URL = 'http://%s/' % env['PRIMARY_HOST']

if 'SERVER_EMAIL' in env:
    SERVER_EMAIL = env['SERVER_EMAIL']

if 'STATIC_URL' in env:
    STATIC_URL = env['STATIC_URL']

if 'STATIC_DIR' in env:
    STATIC_ROOT = env['STATIC_DIR']

if 'MEDIA_URL' in env:
    MEDIA_URL = env['MEDIA_URL']

if 'MEDIA_DIR' in env:
    MEDIA_ROOT = env['MEDIA_DIR']


# Database

if 'DATABASE_URL' in os.environ:
    DATABASES = {'default': dj_database_url.config()}

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': env.get('PGDATABASE', 'app' or APP_NAME),
            'CONN_MAX_AGE': 600,  # number of seconds database connections should persist for

            # User, host and port can be configured by the PGUSER, PGHOST and
            # PGPORT environment variables (these get picked up by libpq).
        }
    }


# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'formatters': {
        'default': {
            'verbose': '[%(asctime)s] (%(process)d/%(thread)d) %(name)s %(levelname)s: %(message)s'
        }
    },
    'loggers': {
        'mriconnect': {
            'handlers':     [],
            'level':        'WARNING',
            'propagate':    False,
            'formatter':    'verbose',
        },
        'django.request': {
            'handlers':     ['mail_admins'],
            'level':        'ERROR',
            'propagate':    False,
            'formatter':    'verbose',
        },
        'django.security': {
            'handlers':     ['mail_admins'],
            'level':        'ERROR',
            'propagate':    False,
            'formatter':    'verbose',
        },
    },
}


if 'LOG_DIR' in env:
    # Error log
    LOGGING['handlers']['errors_file'] = {
        'level':        'WARNING',
        'class':        'logging.handlers.RotatingFileHandler',
        'filename':     os.path.join(env['LOG_DIR'], 'error.log'),
        'maxBytes':     5242880, # 5MB
        'backupCount':  5
    }
    LOGGING['loggers']['django.request']['handlers'].append('errors_file')
    LOGGING['loggers']['django.security']['handlers'].append('errors_file')


RECAPTCHA_PUBLIC_KEY = env["RECAPTCHA_PUBLIC_KEY"]
RECAPTCHA_PRIVATE_KEY = env["RECAPTCHA_PRIVATE_KEY"]

try:
    from .local import *
except ImportError:
    pass
