import os

from django.conf import global_settings

BASE_DIR = os.path.dirname(__file__)

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
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

LANGUAGE_CODE = 'en'

ROOT_URLCONF = 'publications_bootstrap.tests.urls'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

SITE_ID = 1

USE_I18N = True

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
                ],
            },
        },
    ]
