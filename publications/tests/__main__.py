import os
import sys

from django.conf import settings
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

BASE_DIR = os.path.dirname(__file__)
DEBUG = False
INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.staticfiles',
	'publications',
)
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}
MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS += (
	'django.core.context_processors.request',
)

ROOT_URLCONF = 'publications.tests.urls'

settings.configure(
	MEDIA_ROOT=os.path.join(BASE_DIR, 'media'),
	MEDIA_URL='/media/',
	STATIC_ROOT=os.path.join(BASE_DIR, 'static'),
	STATIC_URL='/static/',
	DEBUG=DEBUG,
	INSTALLED_APPS=INSTALLED_APPS,
	DATABASES=DATABASES,
	MIDDLEWARE_CLASSES=MIDDLEWARE_CLASSES,
	TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS,
	ROOT_URLCONF=ROOT_URLCONF)

import django
from distutils.version import StrictVersion

if StrictVersion(django.get_version()) >= StrictVersion('1.7.0'):
	from django import setup
	from django.test.runner import DiscoverRunner
	setup()
	sys.exit(DiscoverRunner(verbosity=1).run_tests(['publications']))
else:
	from django.test.simple import DjangoTestSuiteRunner
	sys.exit(DjangoTestSuiteRunner(verbosity=1).run_tests(['publications.Tests', 'publications.LiveTests']))
