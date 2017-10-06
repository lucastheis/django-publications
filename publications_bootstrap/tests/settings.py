import os
from distutils.version import StrictVersion

import django
from django.conf import global_settings

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

DEBUG = False

SECRET_KEY = 'm+qa*7_8t-=17zt_)9gi)4g%6w*v$xxkh6rwrys*bn9su+5%du'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'ordered_model',

    'publications_bootstrap',
)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

if StrictVersion(django.get_version()) < StrictVersion('1.10.0'):
    MIDDLEWARE_CLASSES = MIDDLEWARE

TIME_ZONE = 'Europe/Zurich'

LANGUAGE_CODE = 'en'

SITE_ID = 1

USE_I18N = True

USE_TZ = True

# MEDIA CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/stable/ref/settings/#media-root
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# See: https://docs.djangoproject.com/en/stable/ref/settings/#media-url
MEDIA_URL = '/media/'

# STATIC FILE CONFIGURATION
# ------------------------------------------------------------------------------
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

ROOT_URLCONF = 'publications_bootstrap.tests.urls'

if hasattr(global_settings, 'TEMPLATE_CONTEXT_PROCESSORS'):
    TEMPLATE_CONTEXT_PROCESSORS = tuple(global_settings.TEMPLATE_CONTEXT_PROCESSORS) + (
        'django.core.context_processors.request',)
else:
    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                ],
            },
        },
    ]
