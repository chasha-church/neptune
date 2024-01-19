#!/usr/bin/env python
import os
from tempfile import mkdtemp

import django
from django.apps import apps

from tests.db import TestDatabasesShim

os.environ['DJANGO_SETTINGS_MODULE'] = 'neptune.settings'

from argparse import ArgumentParser
import sys

from django.conf import settings
from django.test.utils import get_runner


settings.DATABASE_PATH = mkdtemp(
    dir='/dev/shm/' if os.path.isdir('/dev/shm') else None
)

settings.DATABASES = TestDatabasesShim(
    default={
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '%s/%s' % (settings.DATABASE_PATH, '/default',),
    }
)

settings.LOGGING = {}

settings.SUPPRESS_BOUNDARY_EXCEPTION_LOGGING = True

settings.DATABASE_ROUTERS = ['tests.db.TestSFMasterRouter']


class TestSuiteRunner:

    def setup_test_environment(self, *args, **kwargs):
        for model in [model for model in apps.get_models() if not model._meta.managed]:
            model._meta.managed = True

        super(TestSuiteRunner, self).setup_test_environment(**kwargs)

    def teardown_test_environment(self, *args, **kwargs):
        for db_name in settings.DATABASES:
            db_file_path = '%s/%s' % (settings.DATABASE_PATH, db_name,)
            if os.path.exists(db_file_path):
                os.unlink(db_file_path)

        os.rmdir(settings.DATABASE_PATH)
        super(TestSuiteRunner, self).teardown_test_environment(**kwargs)


def runtests(**kwargs):
    test_args = kwargs.pop('test', None) or ['tests']
    kwargs.setdefault('interactive', False)

    TestRunner = get_runner(settings)
    test_runner = TestRunner(**kwargs)
    test_runner.setup_databases()

    failures = test_runner.run_tests(test_args)
    if os.path.exists('.coverage'):
        os.unlink('.coverage')

    sys.exit(failures)


if __name__ == '__main__':
    django.setup()

    parser = ArgumentParser()
    parser.add_argument('test', nargs='*')
    test_arguments = parser.parse_args()

    runtests(**vars(test_arguments))
