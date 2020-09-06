import os
import dj_database_url
import elasticsearch
from requests_aws4auth import AWS4Auth
from django.contrib.messages import constants as messages
import saml2
from saml2.saml import NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED
from saml2.sigver import get_xmlsec_binary

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
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

# email setup
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('EMAIL_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'DALME Project <mail@dalme.org>'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# Application definition
ALLOWED_HOSTS = ['127.0.0.1:8000', '127.0.0.1', 'localhost', '127.0.0.1.xip.io', '127.0.0.1.xip.io:8443', 'db.127.0.0.1.xip.io:8443', 'db.127.0.0.1.xip.io']
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ALLOW_CREDENTIALS = True
# SESSION_COOKIE_SAMESITE = None
SESSION_COOKIE_DOMAIN = '.127.0.0.1.xip.io'
CSRF_COOKIE_DOMAIN = '.127.0.0.1.xip.io'
# SESSION_COOKIE_NAME = 'session_id'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'django.contrib.humanize',
    # 'django.contrib.admindocs',
    'django.contrib.sites',
    'django_hosts',
    'haystack',
    # 'treebeard',
    # 'sekizai',
    'django_celery_results',
    'django_celery_beat',
    # 'allaccess.apps.AllAccessConfig',
    # 'todo',
    # 'debug_toolbar',
    # 'crispy_forms',
    # 'oauth2_provider',
    'djangosaml2idp',
    'corsheaders',
    'rest_framework',
    # 'oidc_provider',
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

ENABLE_DJANGO_EXTENSIONS = bool(int(os.environ.get("ENABLE_DJANGO_EXTENSIONS", "1")))
if DEBUG and ENABLE_DJANGO_EXTENSIONS:
    INSTALLED_APPS += ['django_extensions']

MIDDLEWARE = [
    'django_hosts.middleware.HostsRequestMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # 'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'dalme_app.model_templates.CurrentUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'dalme_app.utils.AsyncMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'oidc_provider.middleware.SessionManagementMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    'django_hosts.middleware.HostsResponseMiddleware'
]

ROOT_HOSTCONF = 'dalme.devHosts'
ROOT_URLCONF = 'dalme.devUrls'
DEFAULT_HOST = 'public'
PARENT_HOST = '127.0.0.1.xip.io:8443'

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
                # 'sekizai.context_processors.sekizai',
                'dalme_public.context_processors.year',
                'dalme_public.context_processors.project',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'dalme.wsgi.application'

# authentication backends
AUTHENTICATION_BACKENDS = [
    # 'allaccess.backends.AuthorizedServiceBackend',
    # 'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend'
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

# OIDC_USERINFO = 'dalme_app.oidc_provider_settings.userinfo'
# OIDC_IDTOKEN_INCLUDE_CLAIMS = True
# OIDC_SESSION_MANAGEMENT_ENABLE = True

# authentication settings
awsauth = AWS4Auth(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, 'es')
# LOGIN_URL = '/accounts/login/dalme_wp/'
LOGIN_URL = 'https://db.127.0.0.1.xip.io:8443/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'https://dalme.org'
# LOGIN_REDIRECT_URL = 'https://db.dalme.org'
# SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# OAUTH2_PROVIDER = {
#     'SCOPES': {'read': 'Read scope', 'write': 'Write scope'}
# }

SAML_IDP_CONFIG = {
    'debug': DEBUG,
    'xmlsec_binary': get_xmlsec_binary(['/opt/local/bin', '/usr/bin/xmlsec1']),
    'entityid': 'https://127.0.0.1.xip.io:8443/idp/metadata',
    'description': 'DALME SAML Identity Provider Setup',
    'service': {
        'idp': {
            'name': 'DALME SAML Identity Provider',
            'endpoints': {
                'single_sign_on_service': [
                    ('https://127.0.0.1.xip.io:8443/idp/sso/post/', saml2.BINDING_HTTP_POST),
                    ('https://127.0.0.1.xip.io:8443/idp/sso/redirect/', saml2.BINDING_HTTP_REDIRECT),
                ],
                "single_logout_service": [
                    ("https://127.0.0.1.xip.io:8443/idp/slo/post/", saml2.BINDING_HTTP_POST),
                    ("https://127.0.0.1.xip.io:8443/idp/slo/redirect/", saml2.BINDING_HTTP_REDIRECT)
                ],
            },
            'name_id_format': [NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED],
            'sign_response': True,
            'sign_assertion': True,
            'want_authn_requests_signed': False,
        },
    },

    # Signing
    'key_file': PROJECT_ROOT + '/ssl-certs/dam.dalme.org.pem',
    'cert_file': PROJECT_ROOT + '/ssl-certs/dam.dalme.org.cert',
    # Encryption
    'encryption_keypairs': [{
        'key_file': PROJECT_ROOT + '/ssl-certs/dam.dalme.org.pem',
        'cert_file': PROJECT_ROOT + '/ssl-certs/dam.dalme.org.cert',
    }],
    'valid_for': 365 * 24,
}


DATABASE_ROUTERS = ['dalme_app.utils.ModelDatabaseRouter']

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
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'read_default_file': os.path.join(BASE_DIR, 'db.cnf'),
                'sql_mode': 'traditional',
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
        }
    }

# Update database configuration with $DATABASE_URL.
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

# HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
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
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'dalme_app.utils.DRFDTEParser',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter'
    ],
    'EXCEPTION_HANDLER': 'dalme_app.utils.DRFDTE_exception_handler',
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

# Media files
DEFAULT_FILE_STORAGE = 'dalme.storage_backends.MediaStorage'
AWS_DEFAULT_ACL = None
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'https://%s/media/' % AWS_S3_CUSTOM_DOMAIN

# Extra places for collectstatic to find static files.
# STATICFILES_DIRS = [
#     os.path.join(PROJECT_ROOT, 'static'),
# ]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "www", 'static')

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SITE_ID = 1
WAGTAIL_SITE_NAME = 'DALME'
WAGTAILIMAGES_IMAGE_MODEL = 'dalme_public.DALMEImage'

# HTTPS/SSL settings
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# CELERY SETUP
# CELERY_BROKER_URL = "sqs://%s:%s@" % (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
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
# CELERY_RESULT_BACKEND = None # Disabling the results backend
CELERY_RESULT_BACKEND = 'django-db'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    }
}

# setting for Debug Toolbar
# INTERNAL_IPS = '127.0.0.1.xip.io'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/dalme_app.log'
        },
        # 'console': {
        #     'class': 'logging.StreamHandler',
        # },
    },
    # 'root': {
    #    'handlers': ['console'],
    #    'level': 'DEBUG',
    # },
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

# MESSAGE_TAGS = {
#     messages.DEBUG: 'alert-info',
#     messages.INFO: 'alert-info',
#     messages.SUCCESS: 'alert-success',
#     messages.WARNING: 'alert-warning',
#     messages.ERROR: 'alert-danger',
# }

MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}

# django-crispy_forms settings
# CRISPY_TEMPLATE_PACK = 'bootstrap4'

if "LOG_TO_STDOUT" in os.environ:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': 'DEBUG',
                'propagate': True,
            },
        },
    }

if "HEROKU_APP_NAME" in os.environ:
    ALLOWED_HOSTS = ["*"]
