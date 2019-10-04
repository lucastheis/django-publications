import os
import sys
from django.conf import settings, global_settings

BASE_DIR = os.path.dirname(__file__)
DEBUG = False
INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.staticfiles',
	'django.contrib.messages',
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

ROOT_URLCONF = 'publications.tests.urls'

settings_dict = {
	'MEDIA_ROOT': os.path.join(BASE_DIR, 'media'),
	'MEDIA_URL': '/media/',
	'STATIC_ROOT': os.path.join(BASE_DIR, 'static'),
	'STATIC_URL': '/static/',
	'DEBUG': DEBUG,
	'INSTALLED_APPS': INSTALLED_APPS,
	'DATABASES': DATABASES,
	'MIDDLEWARE_CLASSES': MIDDLEWARE_CLASSES,
	'ROOT_URLCONF': ROOT_URLCONF}

if hasattr(global_settings, 'TEMPLATE_CONTEXT_PROCESSORS'):
	settings_dict['TEMPLATE_CONTEXT_PROCESSORS'] = \
		tuple(global_settings.TEMPLATE_CONTEXT_PROCESSORS) + ('django.core.context_processors.request',)
else:
	settings_dict['TEMPLATES'] = [
		{
			'BACKEND': 'django.template.backends.django.DjangoTemplates',
			'DIRS': [],
			'APP_DIRS': True,
			'OPTIONS': {
				'context_processors': [
					'django.template.context_processors.request',
					'django.contrib.auth.context_processors.auth',
					'django.contrib.messages.context_processors.messages'
				],
			},
		},
	]

settings_dict['MIDDLEWARE'] = MIDDLEWARE_CLASSES

settings.configure(**settings_dict)

import django

from django import setup
from django.test.runner import DiscoverRunner
setup()
sys.exit(DiscoverRunner(verbosity=1).run_tests(['publications']))
