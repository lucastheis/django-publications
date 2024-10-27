#!/usr/bin/env python3

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'publications.test_settings'

import django
from django.conf import settings
from django.test.utils import get_runner


def main():
	django.setup()

	TestRunner = get_runner(settings)
	test_runner = TestRunner()

	failures = test_runner.run_tests(['publications.settings.test'])

	sys.exit(bool(failures))


if __name__ == '__main__':
	main()
