import os
import sys

from django.conf import settings

BASE_DIR = os.path.dirname(__file__)
DEBUG = False
INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'publications',
)
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}
MIDDLEWARE_CLASSES = (
	'django.middleware.common.CommonMiddleware',
)

settings.configure(
	DEBUG=DEBUG,
	INSTALLED_APPS=INSTALLED_APPS,
	DATABASES=DATABASES,
	MIDDLEWARE_CLASSES=MIDDLEWARE_CLASSES)

import django
from distutils.version import StrictVersion

if StrictVersion(django.get_version()) >= StrictVersion('1.7.0'):
	from django import setup
	from django.test.utils import setup_test_environment
	from django.test.runner import DiscoverRunner
	setup()
	setup_test_environment()
	sys.exit(DiscoverRunner().run_tests(['publications']))
else:
	from django.test.simple import DjangoTestSuiteRunner
	sys.exit(DjangoTestSuiteRunner().run_tests(['publications.Tests'], verbosity=1))
