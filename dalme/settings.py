import os
import dj_database_url
import elasticsearch
from requests_aws4auth import AWS4Auth
from django.contrib.messages import constants as messages

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = os.environ['SECRET_KEY']
AWS_ACCESS_ID = os.environ['AWS_ACCESS_ID']
AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_ES_ENDPOINT = os.environ['AWS_ES_ENDPOINT']
AWS_REGION = os.environ['AWS_DEFAULT_REGION']
AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['EMAIL_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD']
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'DALME Project <mail@dalme.org>'

DEBUG = False
ALLOWED_HOSTS = ['db.dalme.org']

INSTALLED_APPS = [
    'dalme_app.application.DalmeConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'haystack',
    'django_celery_results',
    'rest_framework',
    'oidc_provider',
    'storages'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'dalme_app.middleware.CurrentUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'dalme_app.middleware.AsyncMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dalme.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'dalme.wsgi.application'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

awsauth = AWS4Auth(AWS_ACCESS_ID, AWS_ACCESS_KEY, AWS_REGION, 'es')
OIDC_USERINFO = 'dalme_app.oidc_provider_settings.userinfo'
OIDC_IDTOKEN_INCLUDE_CLAIMS = True
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'https://dalme.org'

DATABASE_ROUTERS = ['dalme_app.db_routers.ModelDatabaseRouter']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['RDS_DB_NAME'],
        'USER': os.environ['RDS_USERNAME'],
        'PASSWORD': os.environ['RDS_PASSWORD'],
        'HOST': os.environ['RDS_HOSTNAME'],
        'PORT': os.environ['RDS_PORT'],
        'CONN_MAX_AGE': 3600,
    },
    'dam': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['DAM_DB_NAME'],
        'USER': os.environ['DAM_USERNAME'],
        'PASSWORD': os.environ['DAM_PASSWORD'],
        'HOST': os.environ['DAM_HOSTNAME'],
    },
    'wiki': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['WIKI_DB_NAME'],
        'USER': os.environ['WIKI_USERNAME'],
        'PASSWORD': os.environ['WIKI_PASSWORD'],
        'HOST': os.environ['WIKI_HOSTNAME'],
    },
    'wp': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ['WP_DB_NAME'],
        'USER': os.environ['WP_USERNAME'],
        'PASSWORD': os.environ['WP_PASSWORD'],
        'HOST': os.environ['WP_HOSTNAME'],
    },
}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
        'URL': AWS_ES_ENDPOINT,
        'INDEX_NAME': 'haystack',
        'KWARGS': {
            'port': 443,
            'http_auth': awsauth,
            'use_ssl': True,
            'verify_certs': True,
            'connection_class': elasticsearch.RequestsHttpConnection,
        }
    },
}

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    )
}

LANGUAGES = [
    ('en', 'English'),
    ('fr', 'French'),
]
LANGUAGE_CODE = 'en'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

DEFAULT_FILE_STORAGE = 'dalme.storage_backends.MediaStorage'
AWS_DEFAULT_ACL = None
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = 'https://%s/media/' % AWS_S3_CUSTOM_DOMAIN
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "www", 'static')

SITE_ID = 1

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CELERY_RESULT_BACKEND = 'db+mysql:///django-db'
CELERY_BROKER_URL = 'redis://localhost'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'include_html': True,
        },
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': '/opt/python/log/dalme_app.log'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
        'dalme_app': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': False
        },
    },
}

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
