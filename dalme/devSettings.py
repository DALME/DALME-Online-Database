"""
For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import dj_database_url
import elasticsearch
from requests_aws4auth import AWS4Auth
from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']
AWS_ACCESS_ID = os.environ['AWS_ACCESS_ID']
AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
AWS_ES_ENDPOINT = os.environ['AWS_ES_ENDPOINT']
AWS_REGION = os.environ['AWS_DEFAULT_REGION']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# Application definition
ALLOWED_HOSTS = ['127.0.0.1:8000','127.0.0.1', 'localhost', '127.0.0.1.xip.io', '127.0.0.1.xip.io:8443']

INSTALLED_APPS = [
    'dalme_app.application.DalmeConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.admindocs',
    'django.contrib.sites',
    'haystack',
    #'treebeard',
    #'sekizai',
    'django_celery_results',
    'allaccess.apps.AllAccessConfig',
    #'todo',
    #'debug_toolbar',
    #'crispy_forms',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'dalme_app.middleware.CurrentUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'dalme_app.middleware.AsyncMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.middleware.locale.LocaleMiddleware'
]


ROOT_URLCONF = 'dalme.devUrls'

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
                #'sekizai.context_processors.sekizai',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'dalme.wsgi.application'

#authentication backends
AUTHENTICATION_BACKENDS = [
    #'allaccess.backends.AuthorizedServiceBackend',
    'django.contrib.auth.backends.ModelBackend'
]

#authentication settings
LOGIN_URL = '/accounts/login/dalme_wp/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'https://dalme.org'
#LOGIN_REDIRECT_URL = 'https://db.dalme.org'

#SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASE_ROUTERS = ['dalme_app.db_routers.ModelDatabaseRouter']

if 'RDS_DB_NAME' in os.environ:
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
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': os.path.join(BASE_DIR, 'db.cnf')
            },
            'TEST': {
                'NAME': 'dalme_app_test',
            },
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

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

awsauth = AWS4Auth(AWS_ACCESS_ID,AWS_ACCESS_KEY,AWS_REGION,'es')

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

#HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

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


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/
LANGUAGES = [
    ('en', 'English'),
    ('fr', 'French'),
]

LANGUAGE_CODE = 'en'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)



# Media files location

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'

# Extra places for collectstatic to find static files.
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SITE_ID = 1

#HTTPS/SSL settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL = 'redis://localhost'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}

#setting for Debug Toolbar
#INTERNAL_IPS = '127.0.0.1.xip.io'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/dalme_app.log'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "www", 'static')

MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}

#django-crispy_forms settings
#CRISPY_TEMPLATE_PACK = 'bootstrap4'
