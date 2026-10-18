#!/usr/bin/env python3

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'publications.settings.test'

import django
from django.conf import settings
from django.test.utils import get_runner


def main():
	django.setup()

	TestRunner = get_runner(settings)
	test_runner = TestRunner()

	test_labels = sys.argv[1:] if len(sys.argv) > 1 else ['publications.tests']
	failures = test_runner.run_tests(test_labels)

	sys.exit(bool(failures))


if __name__ == '__main__':
	main()
