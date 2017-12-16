from os import getenv

import dj_database_url


DEBUG = False

USE_TZ = True

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "djangoratings",
    "tests"
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    }
]

SECRET_KEY = 'adfasdfasdfasdfasdfas'

DATABASES = {
    'default': dj_database_url.config(default=getenv('DATABASE_URL', 'sqlite://db.sql'))
}

SITE_ID = 1
MIDDLEWARE_CLASSES = ()
STATIC_URL = '/static/'
