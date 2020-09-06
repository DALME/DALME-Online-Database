import os
import dj_database_url
import elasticsearch
from requests_aws4auth import AWS4Auth
from django.contrib.messages import constants as messages
import saml2
from saml2.saml import NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED
from saml2.sigver import get_xmlsec_binary

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = os.environ.get('SECRET_KEY', '')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_ES_ENDPOINT = os.environ.get('AWS_ES_ENDPOINT', '')
AWS_REGION = os.environ.get('AWS_DEFAULT_REGION', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
AWS_SQS_URL = os.environ.get('AWS_SQS_QUEUE', '')

SAML_CERT = os.environ.get('SAML_CERT', '')
SAML_KEY = os.environ.get('SAML_KEY', '')

EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'DALME Project <mail@dalme.org>'

DEBUG = False
ALLOWED_HOSTS = ['.dalme.org', 'localhost', '127.0.0.1', '.us-east-1.elasticbeanstalk.com', '.compute-1.amazonaws.com']
CORS_ORIGIN_WHITELIST = ['https://db.dalme.org', 'https://public.dalme.org', 'https://dalme.org', 'https://kb.dalme.org', 'https://dam.dalme.org']
SESSION_COOKIE_DOMAIN = '.dalme.org'
CSRF_COOKIE_DOMAIN = '.dalme.org'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_hosts',
    'haystack',
    'django_celery_results',
    'django_celery_beat',
    'djangosaml2idp',
    'corsheaders',
    'rest_framework',
    'storages',
    'django_filters',
    'modelcluster',
    'taggit',
    'maintenance_mode',
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.routable_page',
    'wagtail.contrib.styleguide',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail.core',
    'wagtailmodelchooser',
    'dalme_app.application.DalmeConfig',
    'dalme_public.application.DalmePublicConfig',
]

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'dalme_app.model_templates.CurrentUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'dalme_app.utils.AsyncMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware'
]

ROOT_URLCONF = 'dalme.urls'
ROOT_HOSTCONF = 'dalme.hosts'
DEFAULT_HOST = 'public'
PARENT_HOST = 'dalme.org'

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
                'dalme_public.context_processors.year',
                'dalme_public.context_processors.project',
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

awsauth = AWS4Auth(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, 'es')
LOGIN_URL = 'https://db.dalme.org/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'https://dalme.org'

SAML_IDP_CONFIG = {
    'xmlsec_binary': get_xmlsec_binary(['/opt/local/bin', '/usr/bin/xmlsec1']),
    'entityid': 'https://db.dalme.org/idp/metadata',
    'description': 'DALME SAML IDP Setup',
    'service': {
        'idp': {
            'name': 'DALME SAML Identity Provider',
            'endpoints': {
                'single_sign_on_service': [
                    ('https://db.dalme.org/idp/sso/post/', saml2.BINDING_HTTP_POST),
                    ('https://db.dalme.org/idp/sso/redirect/', saml2.BINDING_HTTP_REDIRECT),
                ],
                "single_logout_service": [
                    ("https://db.dalme.org/idp/slo/post/", saml2.BINDING_HTTP_POST),
                    ("https://db.dalme.org/idp/slo/redirect/", saml2.BINDING_HTTP_REDIRECT)
                ],
            },
            'name_id_format': [NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED],
            'sign_response': True,
            'sign_assertion': True,
            'want_authn_requests_signed': False,
        },
    },

    # Signing
    'key_file': BASE_DIR + '/ssl-certs/dam.dalme.org.pem',
    'cert_file': BASE_DIR + '/ssl-certs/dam.dalme.org.cert',
    # Encryption
    'encryption_keypairs': [{
        'key_file': BASE_DIR + '/ssl-certs/dam.dalme.org.pem',
        'cert_file': BASE_DIR + '/ssl-certs/dam.dalme.org.cert',
    }],
    'valid_for': 365 * 24,
}

DATABASE_ROUTERS = ['dalme_app.utils.ModelDatabaseRouter']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('RDS_DB_NAME', ''),
        'USER': os.environ.get('RDS_USERNAME', ''),
        'PASSWORD': os.environ.get('RDS_PASSWORD', ''),
        'HOST': os.environ.get('RDS_HOSTNAME', ''),
        'PORT': os.environ.get('RDS_PORT', ''),
        'CONN_MAX_AGE': 3600,
    },
    'dam': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DAM_DB_NAME', ''),
        'USER': os.environ.get('DAM_USERNAME', ''),
        'PASSWORD': os.environ.get('DAM_PASSWORD', ''),
        'HOST': os.environ.get('DAM_HOSTNAME', ''),
    }
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
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'dalme_app.utils.DRFSelectRenderer',
        'dalme_app.utils.DRFDTEJSONRenderer'
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
WAGTAIL_SITE_NAME = 'DALME'
WAGTAILIMAGES_IMAGE_MODEL = 'dalme_public.DALMEImage'

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

CELERY_BROKER_URL = 'sqs://'
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'predefined_queues': {
        'celery': {
            'url': AWS_SQS_URL,
            'access_key_id': AWS_ACCESS_KEY_ID,
            'secret_access_key': AWS_SECRET_ACCESS_KEY,
        }
    }
}
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_BACKEND = 'django-db'

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
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}
