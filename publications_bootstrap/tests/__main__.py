#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

import django
from django.test.runner import DiscoverRunner

os.environ['DJANGO_SETTINGS_MODULE'] = 'publications_bootstrap.tests.settings'

if __name__ == "__main__":
    # https://docs.djangoproject.com/en/1.8/topics/settings/#calling-django-setup-is-required-for-standalone-django-usage

    django.setup()

    sys.exit(DiscoverRunner(verbosity=1).run_tests(['publications_bootstrap']))
