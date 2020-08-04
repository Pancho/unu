import os
import json


here = lambda x: os.path.join(os.path.dirname(os.path.abspath(__file__)), x)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DJANGO_DEBUG') == 'true'  # Better safe than sorry; if not explicitly true, it's false
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.sites',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'raw',
	'unu',
]
MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'djangoutils.urls'
TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': [
			os.path.join(BASE_DIR, 'unu/templates/'),
			os.path.join(BASE_DIR, 'raw/templates/'),
		],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
				'unu.utils.context_processors.mobile.execute',
				'unu.utils.context_processors.grid.execute',
				'unu.utils.context_processors.language.execute',
			],
		},
	},
]
WSGI_APPLICATION = 'djangoutils.wsgi.application'
AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]
LANGUAGE_CODE = 'en-us'
LOCALE_PATHS = [
	os.path.join(BASE_DIR, 'translations/'),
]
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = 'media/'
SITE_ID = 1
ALLOWED_HOSTS = ['localhost', '*']  # For development
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
		'LOCATION': 'memcached:11211',
		'KEY_PREFIX': 'djangoutils',
	}
}
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'standard': {
			'format': '%(asctime)s [%(levelname)s] (%(module)s:%(lineno)d): %(message)s'
		},
	},
	'filters': {
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse'
		},
	},
	'handlers': {
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'standard'
		},
		'default_file': {
			'level': 'INFO',
			'class': 'logging.handlers.RotatingFileHandler',
			'filename': here('../logs/djangoutils.log'),
			'maxBytes': 1024 * 1024 * 100,  # 100 MB
			'backupCount': 10,
			'formatter': 'standard',
		},
	},
	'loggers': {
		'django.request': {
			'handlers': ['default_file'],
			'level': 'WARNING',
			'propagate': True,
		},
		'raw': {
			'handlers': ['console', 'default_file'],
			'level': 'DEBUG',
			'propagate': True,
		},
		'unu': {
			'handlers': ['console', 'default_file'],
			'level': 'DEBUG',
			'propagate': True,
		},
	},
}
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': os.environ.get('DB_NAME'),
		'USER': os.environ.get('DB_USERNAME'),
		'PASSWORD': os.environ.get('DB_PASSWORD'),
		'HOST': 'db',
		'PORT': 5432,
	},
}
MONGO_DB_USERNAME = os.environ.get('MONGO_USERNAME')
MONGO_DB_PASSWORD = os.environ.get('MONGO_PASSWORD')
MONGO_DB_ENDPOINT_URL = 'mongo'
MONGO_DB_ENDPOINT_PORT = 27017
JWT_EXPIRATION_SECONDS = 7 * 24 * 60 * 60
STATIC_FILES_VERSION = os.environ.get('STATIC_FILES_VERSION')

# Unu upgrades
for key, value in os.environ.items():
	if key.startswith('UNU_'):
		globals()[key] = value
