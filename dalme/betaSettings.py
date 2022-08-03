import os
import dj_database_url
import elasticsearch
from requests_aws4auth import AWS4Auth
from django.contrib.messages import constants as messages
import saml2
from saml2.saml import NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED
from saml2.sigver import get_xmlsec_binary

IS_V2 = bool(os.environ.get('V2', False))
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
DOCKER_ROOT = '/app'
HOST = 'https://127.0.0.1.sslip.io:8000'

SECRET_KEY = os.environ.get('SECRET_KEY', '')
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_ES_ENDPOINT = os.environ.get('AWS_ES_ENDPOINT', '')
AWS_REGION = os.environ.get('AWS_DEFAULT_REGION', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY', '')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY', '')

ZOTERO_API_KEY = os.environ.get('ZOTERO_API_KEY', '')
ZOTERO_LIBRARY_ID = os.environ.get('ZOTERO_LIBRARY_ID', '')

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEBUG = True

ALLOWED_HOSTS = ['.127.0.0.1.sslip.io']

USE_HTTPS = True
USE_X_FORWARDED_HOST = True
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_REFERRER_POLICY = 'origin-when-cross-origin'
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_DOMAIN = '.127.0.0.1.sslip.io'

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_DOMAIN = '.127.0.0.1.sslip.io'
SESSION_COOKIE_DOMAIN = '.127.0.0.1.sslip.io'
CSRF_TRUSTED_ORIGINS = ['https://127.0.0.1.sslip.io:8000']

CSRF_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_HTTPONLY = False
SESSION_COOKIE_HTTPONLY = False

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    'https://127.0.0.1.sslip.io',
    'https://127.0.0.1.sslip.io:8000',
]
CORS_EXPOSE_HEADERS = [
    'Content-Type',
    'X-CSRFToken',
    'Access-Control-Allow-Origin: https://127.0.0.1.sslip.io:8000',
]

ROOT_URLCONF = 'dalme.devUrls'
LOGOUT_REDIRECT_URL = 'https://127.0.0.1.sslip.io:8000/'

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'dynamic_preferences',
    'dynamic_preferences.users.apps.UserPreferencesConfig',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_elasticsearch_dsl',
    'django_q',
    'djangosaml2idp',
    'corsheaders',
    'rest_framework',
    'compressor',
    'storages',
    'django_filters',
    'modelcluster',
    'taggit',
    'maintenance_mode',
    'captcha',
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
    'wagtail',
    'wagtailmodelchooser',
    'dalme_api.application.DalmeAPIConfig',
    'dalme_app.application.DalmeConfig',
    'dalme_public.application.DalmePublicConfig',
    'dalme_purl.application.DalmePURLConfig',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'dalme_app.utils.SubdomainRedirectMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'dalme_app.utils.UIAuthMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'dalme_app.utils.AsyncMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'maintenance_mode.middleware.MaintenanceModeMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.csrf',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'dalme_public.context_processors.year',
                'dalme_public.context_processors.project',
                'django.template.context_processors.request',
                'dynamic_preferences.processors.global_preferences',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'dalme.wsgi.application'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend'
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

awsauth = AWS4Auth(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, 'es')

SAML_IDP_CONFIG = {
    'debug': DEBUG,
    'xmlsec_binary': get_xmlsec_binary(['/opt/local/bin', '/usr/bin/xmlsec1']),
    'entityid': 'https://127.0.0.1.sslip.io:8000/idp/metadata',
    'description': 'DALME SAML Identity Provider Setup',
    'service': {
        'idp': {
            'name': 'DALME SAML Identity Provider',
            'endpoints': {
                'single_sign_on_service': [
                    ('https://127.0.0.1.sslip.io:8000/idp/sso/post/', saml2.BINDING_HTTP_POST),
                    ('https://127.0.0.1.sslip.io:8000/idp/sso/redirect/', saml2.BINDING_HTTP_REDIRECT),
                ],
                "single_logout_service": [
                    ("https://127.0.0.1.sslip.io:8000/idp/slo/post/", saml2.BINDING_HTTP_POST),
                    ("https://127.0.0.1.sslip.io:8000/idp/slo/redirect/", saml2.BINDING_HTTP_REDIRECT)
                ],
            },
            'name_id_format': [NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED],
            'sign_response': True,
            'sign_assertion': True,
            'want_authn_requests_signed': False,
        },
    },

    # Signing
    'key_file': f'{DOCKER_ROOT}/ssl-certs/dev-localhost.key',
    'cert_file': f'{DOCKER_ROOT}/ssl-certs/dev-localhost.cert',
    # Encryption
    'encryption_keypairs': [{
        'key_file': f'{DOCKER_ROOT}/ssl-certs/dev-localhost.key',
        'cert_file': f'{DOCKER_ROOT}/ssl-certs/dev-localhost.cert',
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
        # 'CONN_MAX_AGE': 3600, see: https://github.com/Koed00/django-q/issues/435
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1",
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

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

ELASTICSEARCH_DSL = {
    'default': {
        'host': AWS_ES_ENDPOINT,
        'port': 443,
        'http_auth': awsauth,
        'use_ssl': True,
        'verify_certs': True,
        'connection_class': elasticsearch.RequestsHttpConnection,
        'timeout': 360,  # Custom timeout
    },
}
ELASTICSEARCH_DSL_AUTOSYNC = True
ELASTICSEARCH_DSL_AUTO_REFRESH = True
ELASTICSEARCH_DSL_SIGNAL_PROCESSOR = 'django_elasticsearch_dsl.signals.RealTimeSignalProcessor'
SEARCH_RESULTS_PER_PAGE = 10

JSON_PARSER = 'djangorestframework_camel_case.parser.CamelCaseJSONParser' if IS_V2 else 'rest_framework.parsers.JSONParser'
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
        'dalme_api.renderers.SelectRenderer',
        'dalme_api.renderers.DTEJSONRenderer',
        'dalme_api.renderers.DBRenderer'
    ],
    'DEFAULT_PARSER_CLASSES': [
        JSON_PARSER,
        'dalme_api.parsers.DTEParser',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'dalme_api.filter_backends.DalmeOrderingFilter'
    ],
    'EXCEPTION_HANDLER': 'dalme_api.utils.DTE_exception_handler',
    'JSON_UNDERSCOREIZE': {
        'no_underscore_before_number': True,
    },
}


DYNAMIC_PREFERENCES = {
    'MANAGER_ATTRIBUTE': 'preferences',
    'REGISTRY_MODULE': 'preferences',
    'ADMIN_ENABLE_CHANGELIST_FORM': False,
    'SECTION_KEY_SEPARATOR': '__',
    'ENABLE_CACHE': False,
    'VALIDATE_NAMES': True,
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
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = 'https://%s/media/' % AWS_S3_CUSTOM_DOMAIN

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "www", 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False
COMPRESS_STORAGE = 'compressor.storage.BrotliCompressorFileStorage'
COMPRESS_FILTERS = {
    'css': ['compressor.filters.cssmin.rCSSMinFilter'],
    'js': ['compressor.filters.jsmin.JSMinFilter']
}
COMPRESS_OFFLINE_CONTEXT = 'dalme_app.utils.offline_context_generator'

SITE_ID = 1
WAGTAIL_SITE_NAME = 'DALME'
WAGTAILIMAGES_IMAGE_MODEL = 'dalme_public.DALMEImage'
WAGTAILADMIN_BASE_URL = '127.0.0.1.sslip.io:8000/cms'

Q_CLUSTER = {
    'name': 'dalme_q_dev',
    'workers': 2,
    'recycle': 500,
    'timeout': 600,
    'retry': 620,
    'save_limit': 250,
    'queue_limit': 500,
    'bulk': 5,
    'sqs': {
        'aws_region': AWS_REGION,
        'aws_access_key_id': AWS_ACCESS_KEY_ID,
        'aws_secret_access_key': AWS_SECRET_ACCESS_KEY
    }
}

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
            'filename': '/var/log/django/dalme_app.log'
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
