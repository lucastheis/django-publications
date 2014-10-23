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

settings.configure(
	DEBUG=DEBUG,
	INSTALLED_APPS=INSTALLED_APPS,
	DATABASES=DATABASES)

from django.test.simple import DjangoTestSuiteRunner

sys.exit(DjangoTestSuiteRunner().run_tests(['publications.Tests'], verbosity=1))
