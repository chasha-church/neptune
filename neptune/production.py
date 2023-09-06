import os
from pathlib import Path

import pymysql

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False

ENVIRONMENT_NAME = 'Production Heroku'

ALLOWED_HOSTS = ['*']

pymysql.install_as_MySQLdb()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'TEST': {
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    },

    'develop': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DEVELOP_NAME'),
        'USER': os.environ.get('DEVELOP_USER'),
        'PASSWORD': os.environ.get('DEVELOP_PASSWORD'),
        'HOST': os.environ.get('DEVELOP_HOST'),
        'PORT': '3306',
    }
}

try:
    from .settings import *
except ImportError:
    pass
