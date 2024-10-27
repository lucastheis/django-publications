from pathlib import Path

SECRET_KEY = 'test#ca=(=^t8h1a*1ee65_%m$sr38vdd_)!riw9rs17we41no4l3yd'

BASE_DIR = Path(__file__).resolve().parent

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
		'NAME': ':memory:',
	}
}

MIDDLEWARE = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'publications.tests.urls'

STATIC_URL = '/static/'
STATICFILES_DIRS = []
STATIC_ROOT = BASE_DIR / 'build' / 'static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'build/media/'  # Where user uploads live during development.

TEMPLATES = [
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

STORAGES = {
	'default': {
		'BACKEND': 'django.core.files.storage.FileSystemStorage',
		'OPTIONS': {
			'location': MEDIA_ROOT,
			'base_url': MEDIA_URL,
		},
	},
	'staticfiles': {
		'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage',
	},
}

