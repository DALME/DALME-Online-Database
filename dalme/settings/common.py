import os
import dj_database_url
import elasticsearch
from requests_aws4auth import AWS4Auth
from django.contrib.messages import constants as messages
import saml2
from saml2.saml import NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED
from saml2.sigver import get_xmlsec_binary
from datetime import timedelta

# Environment variables
SECRET_KEY = os.environ.get('SECRET_KEY', '')
HOSTNAME = os.environ.get('HOST', '127.0.0.1.sslip.io:8000')  # defaults to development host
HOST = HOSTNAME.split(':')[0] if ':' in HOSTNAME else HOSTNAME
HOST_PORT = f":{HOSTNAME.split(':')[1]}" if ':' in HOSTNAME else ''
DEBUG = bool(os.environ.get('DEBUG', 1))  # defaults to development setting
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '')
AWS_ES_ENDPOINT = os.environ.get('AWS_ES_ENDPOINT', '')
AWS_REGION = os.environ.get('AWS_DEFAULT_REGION', '')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME', '')
AWS_SQS_QUEUE = os.environ.get('AWS_SQS_QUEUE', 'dalme_q_dev')  # defaults to development queue
AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
ZOTERO_API_KEY = os.environ.get('ZOTERO_API_KEY', '')
ZOTERO_LIBRARY_ID = os.environ.get('ZOTERO_LIBRARY_ID', '')
RECAPTCHA_PUBLIC_KEY = os.environ.get('RECAPTCHA_PUBLIC_KEY', '')
RECAPTCHA_PRIVATE_KEY = os.environ.get('RECAPTCHA_PRIVATE_KEY', '')
EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD', '')
ENABLE_DJANGO_EXTENSIONS = bool(int(os.environ.get("ENABLE_DJANGO_EXTENSIONS", "0")))
DB_NAME = os.environ.get('RDS_DB_NAME', os.environ.get('MYSQL_DATABASE', ''))
DB_USER = os.environ.get('RDS_USERNAME', os.environ.get('MYSQL_USER', ''))
DB_PASSWORD = os.environ.get('RDS_PASSWORD', os.environ.get('MYSQL_PASSWORD', ''))
DB_HOST = os.environ.get('RDS_HOSTNAME', os.environ.get('MYSQL_HOST', ''))
DB_PORT = os.environ.get('RDS_PORT', os.environ.get('MYSQL_PORT', ''))
DAM_DB_NAME = os.environ.get('DAM_DB_NAME', '')
DAM_DB_USER = os.environ.get('DAM_USERNAME', '')
DAM_DB_PASSWORD = os.environ.get('DAM_PASSWORD', '')
DAM_DB_HOST = os.environ.get('DAM_HOSTNAME', '')

# Routing
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCKER_ROOT = '/app'
LOGIN_URL = f'https://{HOST}{HOST_PORT}/db/'
LOGOUT_URL = f'https://{HOST}{HOST_PORT}/db/?logout=true'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = f'https://{HOST}{HOST_PORT}/'
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = 'https://%s/media/' % AWS_S3_CUSTOM_DOMAIN
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "www", 'static')
WAGTAILADMIN_BASE_URL = f'{HOST}{HOST_PORT}/cms'

# Defaults
ROOT_URLCONF = 'dalme.urls'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
WSGI_APPLICATION = 'dalme.wsgi.application'
LANGUAGES = [
    ('en', 'English'),
    ('fr', 'French'),
]
LANGUAGE_CODE = 'en'
TIME_ZONE = 'America/New_York'
USE_I18N = True
USE_L10N = True
USE_TZ = True
MESSAGE_TAGS = {
    messages.DEBUG: 'info',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'error',
}

# CSRF
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_DOMAIN = f'.{HOST}'
CSRF_TRUSTED_ORIGINS = [f'https://{HOST}{HOST_PORT}']
CSRF_COOKIE_HTTPONLY = True

# Session
ALLOWED_HOSTS = [
    f'.{HOST}',
    'localhost',
    '127.0.0.1'
]
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_DOMAIN = f'.{HOST}'
SESSION_COOKIE_HTTPONLY = True
SECURE_SSL_REDIRECT = True
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_REFERRER_POLICY = 'origin-when-cross-origin'

# JWT
REST_SESSION_LOGIN = False
REST_USE_JWT = True
JWT_AUTH_COOKIE = 'dalme-access-token'
JWT_AUTH_REFRESH_COOKIE = 'dalme-refresh-token'
JWT_AUTH_REFRESH_COOKIE_PATH = '/api/jwt/token/refresh/'
JWT_AUTH_SECURE = True
JWT_AUTH_HTTPONLY = True
JWT_AUTH_SAMESITE = 'Strict'
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
}


# Apps, middleware, and templates
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_elasticsearch_dsl',
    'django_q',
    'djangosaml2idp',
    'dj_rest_auth',
    'rest_framework',
    'rest_framework.authtoken',
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

if DEBUG and ENABLE_DJANGO_EXTENSIONS:
    INSTALLED_APPS += ['django_extensions']

MIDDLEWARE = [
    'dalme_app.utils.SubdomainRedirectMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'dalme_app.utils.JWTSessionAuthentication',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_currentuser.middleware.ThreadLocalUserMiddleware',
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
            ],
            'debug': DEBUG,
        },
    },
]

# Authentication
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]
AWSAUTH = AWS4Auth(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, 'es')

# SAML Setup
SAML_IDP_CONFIG = {
    'debug': DEBUG,
    'xmlsec_binary': get_xmlsec_binary(['/opt/local/bin', '/usr/bin/xmlsec1']),
    'entityid': f'https://{HOST}{HOST_PORT}/idp/metadata',
    'description': 'DALME SAML IDP Setup',
    'service': {
        'idp': {
            'name': 'DALME SAML Identity Provider',
            'endpoints': {
                'single_sign_on_service': [
                    (f'https://{HOST}{HOST_PORT}/idp/sso/post/', saml2.BINDING_HTTP_POST),
                    (f'https://{HOST}{HOST_PORT}/idp/sso/redirect/', saml2.BINDING_HTTP_REDIRECT),
                ],
                'single_logout_service': [
                    (f'https://{HOST}{HOST_PORT}/idp/slo/post/', saml2.BINDING_HTTP_POST),
                    (f'https://{HOST}{HOST_PORT}/idp/slo/redirect/', saml2.BINDING_HTTP_REDIRECT)
                ],
            },
            'name_id_format': [NAMEID_FORMAT_EMAILADDRESS, NAMEID_FORMAT_UNSPECIFIED],
            'sign_response': True,
            'sign_assertion': True,
            'want_authn_requests_signed': False,
        },
    },

    # Signing
    'key_file': f'{DOCKER_ROOT}/ssl-certs/dam.dalme.org.pem',
    'cert_file': f'{DOCKER_ROOT}/ssl-certs/dam.dalme.org.cert',
    # Encryption
    'encryption_keypairs': [{
        'key_file': f'{DOCKER_ROOT}/ssl-certs/dam.dalme.org.pem',
        'cert_file': f'{DOCKER_ROOT}/ssl-certs/dam.dalme.org.cert',
    }],
    'valid_for': 365 * 24,
}

# Databases
DATABASE_ROUTERS = ['dalme_app.utils.ModelDatabaseRouter']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT,
        # 'CONN_MAX_AGE': 3600, see: https://github.com/Koed00/django-q/issues/435
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES', innodb_strict_mode=1",
        },
    },
    'dam': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DAM_DB_NAME,
        'USER': DAM_DB_USER,
        'PASSWORD': DAM_DB_PASSWORD,
        'HOST': DAM_DB_HOST,
    }
}

DATABASES['default'].update(dj_database_url.config(conn_max_age=500))  # ??

# Elastic Search
ELASTICSEARCH_DSL = {
    'default': {
        'host': AWS_ES_ENDPOINT,
        'port': 443,
        'http_auth': AWSAUTH,
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

# Django DRF
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 25,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        #'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication'
    ),
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'dalme_api.renderers.SelectRenderer',
        'dalme_api.renderers.DBRenderer'
    ],
    'DEFAULT_PARSER_CLASSES': [
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'dalme_api.filter_backends.DalmeOrderingFilter'
    ],
    'JSON_UNDERSCOREIZE': {
        'no_underscore_before_number': True,
    },
}

# JWT setup
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'dalme_app.utils.JWTUserDetailsSerializer',
}

# Static and media file configuration
DEFAULT_FILE_STORAGE = 'dalme.storage_backends.MediaStorage'
AWS_DEFAULT_ACL = None
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
COMPRESS_STORAGE = 'compressor.storage.BrotliCompressorFileStorage'
COMPRESS_OFFLINE_CONTEXT = 'dalme_app.utils.offline_context_generator'
COMPRESS_FILTERS = {
    'css': ['compressor.filters.cssmin.rCSSMinFilter'],
    'js': ['compressor.filters.jsmin.JSMinFilter']
}

# Wagtail configuration
SITE_ID = 1
WAGTAIL_SITE_NAME = 'DALME'
WAGTAILIMAGES_IMAGE_MODEL = 'dalme_public.DALMEImage'

# Background workers (django-q)
Q_CLUSTER = {
    'name': AWS_SQS_QUEUE,
    'workers': 2,
    'recycle': 500,
    'timeout': 600,
    'retry': 620,
    'save_limit': 250,
    'queue_limit': 50,
    'bulk': 5,
    'daemonize_workers': True,
    'sqs': {
        'aws_region': AWS_REGION,
        'aws_access_key_id': AWS_ACCESS_KEY_ID,
        'aws_secret_access_key': AWS_SECRET_ACCESS_KEY
    }
}
