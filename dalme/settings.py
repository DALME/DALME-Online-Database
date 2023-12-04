"""DALME application settings hierarchy.

Uses: https://github.com/jazzband/django-configurations

"""
import dataclasses
import enum
import json
import os
from pathlib import Path

import elasticsearch
import structlog
from configurations import Configuration, pristinemethod, values


@dataclasses.dataclass
class TENANT:
    """Structure for defining application tenants."""

    domain: str
    name: str
    schema_name: str

    def __iter__(self):
        """Allow destructuring assignment."""
        return iter(dataclasses.astuple(self))


class Base(Configuration):
    """Common, inherited settings."""

    @classmethod
    def setup(cls):
        """Override settings setup hook."""
        super().setup()
        cls.INSTALLED_APPS = [
            *cls.SHARED_APPS,
            *[app for app in cls.TENANT_APPS if app not in cls.SHARED_APPS],
        ]

    BASE_DIR = Path(__file__).resolve().parent.parent
    PROJECT_ROOT = BASE_DIR / 'dalme'

    LANGUAGES = [('en', 'English'), ('fr', 'French')]
    LANGUAGE_CODE = 'en'
    LOGIN_REDIRECT_URL = '/'
    LOGIN_URL = '/db/'
    LOGOUT_REDIRECT_URL = '/'
    LOGOUT_URL = '/db/?logout=true'
    ROOT_URLCONF = 'dalme.urls'
    TIME_ZONE = 'America/New_York'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    WSGI_APPLICATION = 'dalme.wsgi.application'

    CORS_ALLOW_CREDENTIALS = True
    CORS_EXPOSE_HEADERS = ['Content-Type', 'X-CSRFToken']
    CSRF_COOKIE_HTTPONLY = False
    SESSION_COOKIE_HTTPONLY = True
    USE_X_FORWARDED_HOST = True

    STATICFILES_DIRS = [
        (BASE_DIR / 'static').as_posix(),
    ]
    MULTITENANT_STATICFILES_DIRS = [
        (BASE_DIR / 'tenants/%s/static').as_posix(),
    ]
    STATICFILES_FINDERS = [
        'django_tenants.staticfiles.finders.TenantFileSystemFinder',  # NOTE: Must come first.
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]
    MULTITENANT_RELATIVE_STATIC_ROOT = ''
    MULTITENANT_RELATIVE_MEDIA_ROOT = ''
    STATIC_URL = '/static/'
    MEDIA_URL = '/media/'

    SHARED_APPS = [
        'django_tenants',
        'ida.apps.IDAConfig',  # App containing the Tenant model.
        'django.contrib.contenttypes',
        # NOTE: The above must be present for django-tenants to function.
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'django_elasticsearch_dsl',
        'rest_framework',
        'django_filters',
        'maintenance_mode',
        'captcha',
        'corsheaders',
        # 'oauth2_provider',
        'dalme_app.application.DalmeConfig',
        'dalme_api.application.DalmeAPIConfig',
        'dalme_purl.application.DalmePURLConfig',
    ]
    TENANT_APPS = [
        'django_filters',
        'modelcluster',
        'taggit',
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
        'dalme_public.application.DalmePublicConfig',
    ]

    MIDDLEWARE = [
        'ida.middleware.HealthCheckMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'ida.middleware.TenantMiddleware',
        'ida.middleware.TenantContextMiddleware',
        'django_structlog.middlewares.RequestMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'dalme_app.utils.SubdomainRedirectMiddleware',
        'django_structlog.middlewares.RequestMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django_currentuser.middleware.ThreadLocalUserMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'maintenance_mode.middleware.MaintenanceModeMiddleware',
        'wagtail.contrib.redirects.middleware.RedirectMiddleware',
    ]

    @property
    def TEMPLATES(self):  # noqa: N802
        return [
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [
                    (self.BASE_DIR / 'templates').as_posix(),
                ],
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
                    'debug': self.DEBUG,
                    'loaders': [
                        'django_tenants.template.loaders.filesystem.Loader',  # NOTE: Must come first.
                        'django.template.loaders.filesystem.Loader',
                        'django.template.loaders.app_directories.Loader',
                    ],
                },
            },
        ]

    @property
    def MULTITENANT_TEMPLATE_DIRS(self):  # noqa: N802
        return [
            (self.BASE_DIR / 'tenants/%s/templates').as_posix(),
        ]

    DATABASE_ROUTERS = [
        'dalme_app.utils.ModelDatabaseRouter',
        'django_tenants.routers.TenantSyncRouter',
    ]
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
    AUTH_USER_MODEL = 'auth.User'
    TENANT_DOMAIN_MODEL = 'ida.Domain'
    TENANT_MODEL = 'ida.Tenant'

    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'colored_console': {
                '()': structlog.stdlib.ProcessorFormatter,
                'processor': structlog.dev.ConsoleRenderer(colors=True),
            },
            'json_formatter': {
                '()': structlog.stdlib.ProcessorFormatter,
                'processor': structlog.processors.JSONRenderer(),
            },
            'key_value': {
                '()': structlog.stdlib.ProcessorFormatter,
                'processor': structlog.processors.KeyValueRenderer(
                    key_order=['timestamp', 'level', 'event', 'logger'],
                ),
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'colored_console',
            },
            'flat_line': {
                'class': 'logging.StreamHandler',
                'formatter': 'key_value',
            },
            'json': {
                'class': 'logging.StreamHandler',
                'formatter': 'json_formatter',
            },
            'null': {
                'class': 'logging.NullHandler',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': LOG_LEVEL,
        },
        'loggers': {
            'django_structlog': {
                'level': LOG_LEVEL,
            },
            'dalme': {
                'level': LOG_LEVEL,
            },
            'dalme_api': {
                'level': LOG_LEVEL,
            },
            'dalme_app': {
                'level': LOG_LEVEL,
            },
            'dalme_public': {
                'level': LOG_LEVEL,
            },
            'gunicorn.access': {
                'level': LOG_LEVEL,
            },
            'gunicorn.error': {
                'level': LOG_LEVEL,
            },
            # Nulled to use structlog middleware.
            'django.server': {
                'handlers': ['null'],
                'propagate': False,
            },
            'django.request': {
                'handlers': ['null'],
                'propagate': False,
            },
        },
    }

    AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.ModelBackend']
    AUTH_PASSWORD_VALIDATORS = [
        {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
        {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
        {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
        {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
    ]

    REST_FRAMEWORK = {
        'DEFAULT_PAGINATION_CLASS': 'dalme_api.paginators.DALMELimitOffsetPagination',
        'PAGE_SIZE': 10,
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.TokenAuthentication',
        ],
        'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_RENDERER_CLASSES': [
            'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ],
        'DEFAULT_PARSER_CLASSES': [
            'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        ],
        'DEFAULT_FILTER_BACKENDS': [
            'django_filters.rest_framework.DjangoFilterBackend',
            'rest_framework.filters.SearchFilter',
            'dalme_api.filter_backends.DalmeOrderingFilter',
        ],
        'JSON_UNDERSCOREIZE': {
            'no_underscore_before_number': True,
        },
    }

    # Elasticsearch
    ELASTICSEARCH_DSL_AUTOSYNC = True
    ELASTICSEARCH_DSL_AUTO_REFRESH = True
    ELASTICSEARCH_DSL_SIGNAL_PROCESSOR = 'django_elasticsearch_dsl.signals.RealTimeSignalProcessor'
    SEARCH_RESULTS_PER_PAGE = 10

    # Wagtail
    SITE_ID = 1
    WAGTAILADMIN_BASE_URL = 'cms/'
    WAGTAILIMAGES_IMAGE_MODEL = 'dalme_public.DALMEImage'

    # Zotero
    ZOTERO_API_KEY = os.environ.get('ZOTERO_API_KEY', '')
    ZOTERO_LIBRARY_ID = os.environ.get('ZOTERO_LIBRARY_ID', '')

    @pristinemethod
    def TENANTS(self):  # noqa: N802
        """Enumerate registered app tenants.

        This is just reference data that is used to setup and migrate the
        database schema to the correct state. Use the full Tenant model in any
        actual application business logic.

        Because enums are actually callable after they are instantiated (you
        can call `SomeEnum('value')` and it's allowed, but if you call
        `SomeEnum()` it'll throw an exception) django-configurations barfs when
        we set a bare enum as a setting because it tries to call it without an
        argument when it parses and checks the settings. This seems to be a
        bug, it doesn't look like they have even considered that anyone would
        use an enum as a setting at this point. This being the case we can just
        wrap TENANTS in `pristinemethod` here which means that it doesn't
        undergo the `callable` check (which is skipped for `pristinemethod`)
        which would otherwise break startup.

        The expense is that we actually have to call `settings.TENANTS()` in
        the app whenever we need it. We could just make TENANTS a dict to avoid
        this but I prefer to pass around a value with the full typing of a
        struct/enum so we can just pay that price until enums are first-class
        citizens in django-configurations.

        See below for details:

          - https://docs.python.org/3/howto/enum.html
          - https://github.com/jazzband/django-configurations/blob/cad6dcb7f00c26702e5c5305901712409b94c848/configurations/importer.py#L163

        For adding Tenants to an existing environment update the tenant data
        provided in the environment and use the mangement command
        'ensure_tenants'. This doesn't need to be done manually, the  command
        runs idempotently on each deployment of the app to the ECS service.

        """
        tenants = os.environ.get('TENANTS', self._TENANTS)
        if isinstance(tenants, str):
            tenants = json.loads(tenants)

        return enum.Enum('TENANTS', {key: TENANT(**tenant_data) for key, tenant_data in tenants.items()})


class Development(Base, Configuration):
    """Development settings."""

    @classmethod
    def setup(cls):
        super().setup()
        cls.INSTALLED_APPS += ['django_extensions']

    DEBUG = True
    DOTENV = os.environ.get('ENV_FILE')

    ALLOWED_HOSTS = [
        'dalme.localhost',
        'globalpharmacopeias.localhost',
    ]

    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOWED_ORIGINS = [
        'http://dalme.localhost:8000',
        'http://globalpharmacopeias.localhost:8000',
    ]

    CSRF_COOKIE_SECURE = False
    CSRF_TRUSTED_ORIGINS = [
        'http://dalme.localhost:8000',
        'http://globalpharmacopeias.localhost:8000',
    ]
    SESSION_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    SECRET_KEY = 'django-insecure-development-environment-secret-key'

    @property
    def MEDIA_ROOT(self):  # noqa: N802
        return (self.BASE_DIR / 'www' / 'media').as_posix()

    @property
    def STATIC_ROOT(self):  # noqa: N802
        return (self.BASE_DIR / 'www' / 'static').as_posix()

    DATABASES = {
        'default': {
            'ENGINE': 'django_tenants.postgresql_backend',
            'NAME': os.environ['POSTGRES_DB'],
            'USER': os.environ['POSTGRES_USER'],
            'PASSWORD': os.environ['POSTGRES_PASSWORD'],
            'HOST': os.environ['POSTGRES_HOST'],
            'PORT': os.environ.get('POSTGRES_PORT', 5432),
            'TEST': {
                'NAME': 'test_dalme_db',
            },
        },
        'dam': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': values.Value('DAM_DB_NAME', environ_prefix=None),
            'USER': values.Value('DAM_DB_USER', environ_prefix=None),
            'PASSWORD': values.Value('DAM_DB_PASSWORD', environ_prefix=None),
            'HOST': values.Value('DAM_DB_HOST', environ_prefix=None),
            'PORT': os.environ.get('DAM_DB_PORT', 3306),
        },
    }

    # https://docs.djangoproject.com/en/4.2/ref/settings/#storages
    STORAGES = {
        'default': {
            'BACKEND': 'django_tenants.files.storage.TenantFileSystemStorage',
        },
        'staticfiles': {
            'BACKEND': 'django_tenants.staticfiles.storage.TenantStaticFilesStorage',
        },
    }

    RECAPTCHA_PUBLIC_KEY = 'django-insecure-development-environment-recaptcha-public-key'
    RECAPTCHA_PRIVATE_KEY = 'django-insecure-development-environment-recaptcha-private-key'

    ELASTICSEARCH_DSL = {
        'default': {
            'hosts': os.environ.get('ELASTICSEARCH_ENDPOINT', 'dalme.es:9200'),
        },
    }

    _TENANTS = {
        'DALME': {
            'domain': 'dalme.localhost',
            'name': 'DALME',
            'schema_name': 'dalme',
        },
        'GLOBALPHARMACOPEIAS': {
            'domain': 'globalpharmacopeias.localhost',
            'name': 'Global Pharmacopeias',
            'schema_name': 'globalpharmacopeias',
        },
    }


class CI(Development, Configuration):
    """Continuous integration pipeline settings."""

    @classmethod
    def setup(cls):
        super().setup()

    DEBUG = False
    SECRET_KEY = 'django-insecure-continuous-integration-environment-secret-key'


class Production(Base, Configuration):
    """Production settings."""

    @classmethod
    def setup(cls):
        super().setup()
        cls.INSTALLED_APPS += ['storages']
        cls.LOGGING['root']['handlers'] = ['flat_line']

    DEBUG = False

    # NOTE: By property-izing these env values we make their evaluation lazy
    # and we don't need to also set them in the development environment, which
    # keeps everything simpler. If we don't do this we'll get KeyError at app
    # startup time if anything is unset when the classes are evaluated. We
    # could of course use `os.environ.get` but I much prefer to see a KeyError
    # thrown at deploy time if I've forgotten to set a value in the environment
    # instead having to trace some runtime error much further down the line.
    @property
    def ALLOWED_HOSTS(self):  # noqa: N802
        return json.loads(os.environ['ALLOWED_HOSTS'])

    @property
    def AWS_S3_CUSTOM_DOMAIN(self):  # noqa: N802
        return f'{self.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

    @property
    def AWS_STORAGE_BUCKET_NAME(self):  # noqa: N802
        return os.environ['AWS_STORAGE_BUCKET_NAME']

    @property
    def CORS_ALLOWED_ORIGINS(self):  # noqa: N802
        return [f'https://{domain}' for domain in self.TENANT_DOMAINS]

    @property
    def CSRF_TRUSTED_ORIGINS(self):  # noqa: N802
        return [f'https://{domain}' for domain in self.TENANT_DOMAINS]

    @property
    def DATABASES(self):  # noqa: N802
        return {
            'default': {
                'ENGINE': 'django_tenants.postgresql_backend',
                'NAME': os.environ['POSTGRES_DB'],
                'USER': os.environ['POSTGRES_USER'],
                'PASSWORD': os.environ['POSTGRES_PASSWORD'],
                'HOST': os.environ['POSTGRES_HOST'],
                'PORT': 5432,
            },
            'dam': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.environ.get('DAM_DB_NAME'),
                'USER': os.environ.get('DAM_DB_USER'),
                'PASSWORD': os.environ.get('DAM_DB_PASSWORD'),
                'HOST': os.environ.get('DAM_DB_HOST'),
                'PORT': 3306,
            },
        }

    @property
    def ELASTICSEARCH_DSL(self):  # noqa: N802
        return {
            'default': {
                'host': os.environ['ELASTICSEARCH_ENDPOINT'],
                'port': 443,
                'http_auth': (
                    os.environ['ELASTICSEARCH_USER'],
                    os.environ['ELASTICSEARCH_PASSWORD'],
                ),
                'use_ssl': True,
                'verify_certs': True,
                'connection_class': elasticsearch.RequestsHttpConnection,
                'timeout': 360,
            },
        }

    @property
    def RECAPTCHA_PUBLIC_KEY(self):  # noqa: N802
        return os.environ.get('RECAPTCHA_PUBLIC_KEY', '')

    @property
    def RECAPTCHA_PRIVATE_KEY(self):  # noqa: N802
        return os.environ.get('RECAPTCHA_PRIVATE_KEY', '')

    @property
    def SECRET_KEY(self):  # noqa: N802
        return os.environ['DJANGO_SECRET_KEY']

    @property
    def MEDIA_URL(self):  # noqa: N802
        return f'https://{self.AWS_S3_CUSTOM_DOMAIN}/{self.MEDIA_LOCATION}/'

    @property
    def STATIC_URL(self):  # noqa: N802
        return f'https://{self.AWS_S3_CUSTOM_DOMAIN}/{self.STATIC_LOCATION}/'

    @property
    def TENANT_DOMAINS(self):  # noqa: N802
        return json.loads(os.environ['TENANT_DOMAINS'])

    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

    SECURE_SSL_REDIRECT = False
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_HSTS_SECONDS = 3600  # TODO: Increase to 31536000 when stable.
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    AWS_DEFAULT_ACL = None
    AWS_IS_GZIPPED = True
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    STATIC_LOCATION = 'static'
    MEDIA_LOCATION = 'media'

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_USE_SSL = False
    EMAIL_PORT = 587
    DEFAULT_FROM_EMAIL = 'DALME <mail@dalme.org>'

    SHOW_PUBLIC_IF_NO_TENANT_FOUND = False

    # https://docs.djangoproject.com/en/4.2/ref/settings/#storages
    STORAGES = {
        'default': {
            'BACKEND': 'dalme.storage_backends.MediaStorage',
        },
        'staticfiles': {
            'BACKEND': 'dalme.storage_backends.StaticStorage',
        },
    }

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
            'LOCATION': 'cache_table',
        },
    }


class Staging(Production, Configuration):
    """Staging settings."""

    @classmethod
    def setup(cls):
        super().setup()

    _TENANTS = {
        'DALME': {
            'domain': 'dalme.ocp.systems',
            'name': 'DALME',
            'schema_name': 'dalme',
        },
        'GLOBALPHARMACOPEIAS': {
            'domain': 'globalpharmacopeias.ocp.systems',
            'name': 'Global Pharmacopeias',
            'schema_name': 'globalpharmacopeias',
        },
    }
