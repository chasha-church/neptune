from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = False

ENVIRONMENT_NAME = 'Staging Heroku'

ALLOWED_HOSTS = ['*']


try:
    from .settings import *
except ImportError:
    pass
