"""
Django settings for mriconnect project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '1han1v%@fd0#e40#tm0z!g2twgo3+!gf9-kr3--1v5)_bkfv4q'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crequest',
    'crispy_forms',
    'reversion',
    'tabular_permissions',
    #'ra',
    #'ra.admin',
    #'ra.activity',
    #'ra.reporting',
    'slick_reporting',
    'jazzmin',

    'django_countries',
    'multiselectfield',
    'people',

    'data_wizard',
    'data_wizard.sources',

    'django.contrib.admin', # comes at the end because the theme is replaced
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'crequest.middleware.CrequestMiddleware',

]

ROOT_URLCONF = 'mriconnect.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'django.template.context_processors.i18n',
                'django.template.context_processors.static',
                'ra.base.context_processors.global_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'mriconnect.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'collected_static')
CRISPY_TEMPLATE_PACK = 'bootstrap4'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',

)

JAZZMIN_SETTINGS = {
    "site_title": "MRI Connect: Experts Database",
    "site_header": "Experts DB",
    "welcome_sign": "Welcome to MRI Connect",
    "copyright": "Mountain Research Initiative",
    "search_model": "people.Person",

    "topmenu_links": [
        {"model": "people.Person"},
        {"app": "data_wizard"},
    ],

    # Side menu
    "hide_apps": ["data_wizard"],

    "changeform_format": "single",
    "language_chooser": True,
    "navigation_expanded": True,
}

JAZZMIN_UI_TWEAKS = {

    "navbar": "navbar-primary navbar-dark",
    "no_navbar_border": True,
    "body_small_text": False,
    "navbar_small_text": False,
    "sidebar_nav_small_text": False,
    "accent": "accent-primary",
    "sidebar": "sidebar-dark-primary",
    "brand_colour": "navbar-primary",
    "brand_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "footer_small_text": False
}

DATA_WIZARD = {
    'BACKEND': 'data_wizard.backends.threading',
    'LOADER': 'data_wizard.loaders.FileLoader',
    'IDMAP': 'data_wizard.idmap.never',   # 'data_wizard.idmap.existing' in 2.0
    'AUTHENTICATION': 'rest_framework.authentication.SessionAuthentication',
    'PERMISSION': 'rest_framework.permissions.IsAdminUser',
}
