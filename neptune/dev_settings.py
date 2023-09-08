from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True

ENVIRONMENT_NAME = 'Devs local'

ALLOWED_HOSTS = ['*']


try:
    from .settings import *
except ImportError:
    pass
