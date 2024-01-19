import os
from pathlib import Path

import pymysql

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-54(#+6q14iay)#lxmfq4^6cjg$g6v7pra0f60ounktz!7^#mxw'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'apiv1',
    'db',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'neptune.urls'


pymysql.install_as_MySQLdb()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'TEST': {
            'NAME': BASE_DIR / 'test_db_sqlite3',
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


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework.filters.SearchFilter',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FileUploadParser',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anonymous_burst': '60/min',
        'anonymous_sustained': '1000/day'
    },
    'DEFAULT_PAGINATION_CLASS': 'apiv1.pagination.DefaultPageNumberPagination',
    'PAGINATE_BY': 100,
    'PAGINATE_BY_PARAM': 'page_size',
    'MAX_PAGINATE_BY': 1000,
    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'ordering',
    'EXCEPTION_HANDLER': 'apiv1.utils.default_exception_handler',
}


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
            ],
        },
    },
]

# Suppress boundary exception logging handled by EXCEPTION_HANDLER during automated testing
SUPPRESS_BOUNDARY_EXCEPTION_LOGGING = False

WSGI_APPLICATION = 'neptune.wsgi.application'


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DB_SERVER_PARAMETER_LIMIT = 2100

AWS_S3_BUCKET_NAME = 'chashaby'
AWS_S3_URL = 'https://{bucket_name}.s3.eu-central-1.amazonaws.com/{file_name}'

CUSTOMER_DOMAIN = 'develop'
