#!/usr/bin/env python
import os
import sys

import django
from django.apps import apps
from django.conf import settings
from django.test.utils import get_runner


def setup_test_environment():
    for model in [model for model in apps.get_models() if not model._meta.managed]:
        model._meta.managed = True


if __name__ == "__main__":
    os.environ["DJANGO_SETTINGS_MODULE"] = "neptune.test_settings"
    django.setup()

    setup_test_environment()

    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(["tests"])
    sys.exit(bool(failures))
