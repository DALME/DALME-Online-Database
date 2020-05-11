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
SECRET_KEY = os.environ['SECRET_KEY']

# email setup
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ['EMAIL_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD']
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'DALME Project <mail@dalme.org>'

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# Application definition
ALLOWED_HOSTS = ['127.0.0.1:8000', '127.0.0.1', 'localhost', '127.0.0.1.xip.io', '127.0.0.1.xip.io:8443']
CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.humanize',
    #'django.contrib.admindocs',
    'django.contrib.sites',
    'haystack',
    #'treebeard',
    #'sekizai',
    'django_celery_results',
    # 'allaccess.apps.AllAccessConfig',
    #'todo',
    #'debug_toolbar',
    #'crispy_forms',
    #'oauth2_provider',
    'djangosaml2idp',
    'corsheaders',
    'rest_framework',
    # 'oidc_provider',
    'storages',
    'django_filters',
    'modelcluster',
    'taggit',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.contrib.routable_page',
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
    # 'corsheaders.middleware.CorsMiddleware',
    #'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.middleware.security.SecurityMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'dalme_app.utils.CurrentUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'dalme_app.utils.AsyncMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'oidc_provider.middleware.SessionManagementMiddleware',
    'wagtail.core.middleware.SiteMiddleware',
    'wagtail.contrib.redirects.middleware.RedirectMiddleware',
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
                'dalme_public.context_processors.year',
                'dalme_public.context_processors.project',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'dalme.wsgi.application'

#authentication backends
AUTHENTICATION_BACKENDS = [
    #'allaccess.backends.AuthorizedServiceBackend',
    #'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend'
]

AUTH_PASSWORD_VALIDATORS = [
    # {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    # {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    # {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    # {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

OIDC_USERINFO = 'dalme_app.oidc_provider_settings.userinfo'
OIDC_IDTOKEN_INCLUDE_CLAIMS = True
OIDC_SESSION_MANAGEMENT_ENABLE = True

#authentication settings
#LOGIN_URL = '/accounts/login/dalme_wp/'
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'https://dalme.org'
#LOGIN_REDIRECT_URL = 'https://db.dalme.org'
BASE_URL = 'https://127.0.0.1.xip.io:8443/idp'
#SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# OAUTH2_PROVIDER = {
#     'SCOPES': {'read': 'Read scope', 'write': 'Write scope'}
# }

SAML_IDP_CONFIG = {
    'debug': DEBUG,
    'xmlsec_binary': get_xmlsec_binary(['/opt/local/bin', '/usr/bin/xmlsec1']),
    'entityid': '%s/metadata' % BASE_URL,
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

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch2_backend.Elasticsearch2SearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack',
    },
}
if 'AWS_ES_ENDPOINT' in os.environ:
    AWS_ES_ENDPOINT = os.environ['AWS_ES_ENDPOINT']
    awsauth = AWS4Auth(
        os.environ['AWS_ACCESS_KEY_ID'],
        os.environ['AWS_SECRET_ACCESS_KEY'],
        os.environ['AWS_DEFAULT_REGION'],
        'es'
    )
    HAYSTACK_CONNECTIONS["default"].update({
        'URL': AWS_ES_ENDPOINT,
        'KWARGS': {
            'port': 443,
            'http_auth': awsauth,
            'use_ssl': True,
            'verify_certs': True,
            'connection_class': elasticsearch.RequestsHttpConnection,
        }
    })

if 'SEARCHBOX_SSL_URL' in os.environ:
    from urllib.parse import urlparse
    es = urlparse(os.environ['SEARCHBOX_SSL_URL'])
    port = es.port or 443
    HAYSTACK_CONNECTIONS['default'].update({
        'URL': es.scheme + '://' + es.hostname + ':' + str(port),
        'KWARGS': {
            'http_auth': es.username + ':' + es.password,
            'use_ssl': True,
            'verify_certs': True,
            'connection_class': elasticsearch.RequestsHttpConnection,
        }
    })


#HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

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
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
if 'AWS_STORAGE_BUCKET_NAME' in os.environ:
    AWS_ACCESS_KEY_ID = os.environ['AWS_ACCESS_KEY_ID']
    AWS_SECRET_ACCESS_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
    DEFAULT_FILE_STORAGE = 'dalme.storage_backends.MediaStorage'

    AWS_STORAGE_BUCKET_NAME = os.environ['AWS_STORAGE_BUCKET_NAME']
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    MEDIA_URL = 'https://%s/media/' % AWS_S3_CUSTOM_DOMAIN

    AWS_DEFAULT_ACL = None
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

# Extra places for collectstatic to find static files.
# STATICFILES_DIRS = [
#     os.path.join(PROJECT_ROOT, 'static'),
# ]
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "www", 'static')

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

SITE_ID = 1

#HTTPS/SSL settings
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


CELERY_BROKER_URL = 'redis://localhost'
CELERY_RESULT_BACKEND = 'django-db'

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




#django-crispy_forms settings
#CRISPY_TEMPLATE_PACK = 'bootstrap4'

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

WAGTAIL_SITE_NAME = 'DALME'
WAGTAILIMAGES_IMAGE_MODEL = 'dalme_public.DALMEImage'
