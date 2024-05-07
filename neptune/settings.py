import os
import sys
from pathlib import Path

import pymysql
import structlog

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
    "django_structlog",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_structlog.middlewares.RequestMiddleware',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        "json_formatter": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
            # https://github.com/jrobichaud/django-structlog/tree/3.0.1#standard-loggers
            # This allows logs from the standard logger to be structured. If you add additional
            # processors to the structlog configuration below you should probably add them here
            # too.
            "foreign_pre_chain": [
                structlog.contextvars.merge_contextvars,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.stdlib.add_logger_name,
                structlog.stdlib.add_log_level,
                structlog.stdlib.PositionalArgumentsFormatter(),
                structlog.processors.StackInfoRenderer(),
                structlog.processors.format_exc_info,
                structlog.processors.UnicodeDecoder(),
            ],
        },
        "plain_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(),
        },
    },
    'handlers': {
        "file": {
            "level": "DEBUG",
            "class": "logging.handlers.WatchedFileHandler",
            "filename": "test.log",
        },
        'console': {
            'class': 'logging.StreamHandler',
            "formatter": "plain_console",
            'stream': sys.stdout,
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'apiv1': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        },
        'db': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'INFO',
        }
    }
}

structlog.configure(
    processors=[
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.filter_by_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

ROOT_URLCONF = 'neptune.urls'


pymysql.install_as_MySQLdb()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
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

USE_TZ = False

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DB_SERVER_PARAMETER_LIMIT = 2100

AWS_S3_BUCKET_NAME = 'chashaby'
AWS_S3_URL = 'https://{bucket_name}.s3.eu-central-1.amazonaws.com/{file_name}'

CUSTOMER_DOMAIN = 'develop'

AZBYKARU_API_LOGIN = os.environ.get('AZBYKARU_API_LOGIN')
AZBYKARU_API_PASSWORD = os.environ.get('AZBYKARU_API_PASSWORD')
AZBYKARU_API_ACCESS_TOKEN = os.environ.get('AZBYKARU_API_ACCESS_TOKEN')
AZBYKARU_BASE_URL = 'https://azbyka.ru/days/api/'


CORS = '*'  # Allow all
CORS_METHODS = ['GET', 'OPTIONS']
CORS_MAX_AGE = 86400    # One day in seconds

TEST_CUSTOMER_DOMAIN = 'default'
