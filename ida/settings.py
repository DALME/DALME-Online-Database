"""IDA application settings hierarchy.

Uses: https://github.com/jazzband/django-configurations

"""

import dataclasses
import enum
import json
import os
from pathlib import Path

import elasticsearch
import structlog
from configurations import Configuration, pristinemethod


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

    IS_DEV = os.environ['ENV'] in {'development', 'ci'}

    BASE_DIR = Path(__file__).resolve().parent.parent
    PROJECT_ROOT = BASE_DIR / 'ida'

    LANGUAGES = [('en', 'English'), ('fr', 'French')]
    LANGUAGE_CODE = 'en'
    LOGIN_REDIRECT_URL = '/'
    LOGIN_URL = '/db/'
    LOGOUT_REDIRECT_URL = '/'
    LOGOUT_URL = '/db/?logout=true'
    ROOT_URLCONF = 'ida.urls'
    TIME_ZONE = 'America/New_York'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True
    WSGI_APPLICATION = 'ida.wsgi.application'

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
        'ida',  # App containing the Tenant model.
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
        'django_recaptcha',
        'corsheaders',
        'oauth2_provider',
        'api',
        'purl',
    ]
    TENANT_APPS = [
        'django_filters',
        'wagtail.contrib.forms',
        'wagtail.contrib.redirects',
        'wagtail.contrib.routable_page',
        'wagtail.contrib.styleguide',
        'wagtail.contrib.table_block',
        'wagtail.contrib.settings',
        'wagtail.embeds',
        'wagtail.sites',
        'wagtail.users',
        'wagtail.snippets',
        'wagtail.documents',
        'wagtail.images',
        'wagtail.search',
        'wagtail.admin',
        'wagtail.api.v2',
        'wagtail',
        'modelcluster',
        'taggit',
        'wagtailmodelchooser',
        'wagtailfontawesomesvg',
        'wagtailcodeblock',
        'public.extensions.team',
        'public.extensions.bibliography',
        'public.extensions.footnotes',
        'public.extensions.gradients',
        'public.extensions.banners',
        'public.extensions.saved_searches',
        'public',
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
        'ida.utils.SubdomainRedirectMiddleware',
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
                        'django.template.context_processors.request',
                        'wagtail.contrib.settings.context_processors.settings',
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
        'ida.utils.ModelDatabaseRouter',
        'django_tenants.routers.TenantSyncRouter',
    ]
    DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
    AUTH_USER_MODEL = 'ida.User'
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
            'ida': {
                'level': LOG_LEVEL,
            },
            'api': {
                'level': LOG_LEVEL,
            },
            'public': {
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
    OAUTH2_PROVIDER_APPLICATION_MODEL = 'ida.Application'
    OAUTH2_ACCESS_TOKEN_EXPIRY = os.environ.get('OAUTH2_ACCESS_TOKEN_EXPIRY', 3600)  # 1 hour
    OAUTH2_REFRESH_TOKEN_COOKIE_EXPIRY = os.environ.get('OAUTH2_REFRESH_TOKEN_COOKIE_EXPIRY', 3600 * 24 * 14)  # 14 days

    @property
    def OAUTH_CLIENT_ID(self):  # noqa: N802
        return os.environ['OAUTH_CLIENT_ID']

    @property
    def OAUTH_CLIENT_SECRET(self):  # noqa: N802
        return os.environ['OAUTH_CLIENT_SECRET']

    REST_FRAMEWORK = {
        'DEFAULT_FILTER_BACKENDS': [
            'django_filters.rest_framework.DjangoFilterBackend',
            'rest_framework.filters.SearchFilter',
            'api.filter_backends.IDAOrderingFilter',
        ],
        'DEFAULT_PAGINATION_CLASS': 'api.paginators.IDALimitOffsetPagination',
        'DEFAULT_PARSER_CLASSES': [
            'djangorestframework_camel_case.parser.CamelCaseJSONParser',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticated',
        ],
        'DEFAULT_RENDERER_CLASSES': [
            'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ],
        'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
        'JSON_UNDERSCOREIZE': {
            'no_underscore_before_number': True,
        },
        'PAGE_SIZE': 10,
    }

    # Elasticsearch
    ELASTICSEARCH_DSL_AUTOSYNC = True
    ELASTICSEARCH_DSL_AUTO_REFRESH = True
    ELASTICSEARCH_DSL_SIGNAL_PROCESSOR = 'django_elasticsearch_dsl.signals.RealTimeSignalProcessor'
    SEARCH_RESULTS_PER_PAGE = 10

    # Wagtail
    SITE_ID = 1
    WAGTAILADMIN_BASE_URL = 'cms/'
    WAGTAILIMAGES_IMAGE_MODEL = 'public.BaseImage'

    # reference urls
    BASE_URL = 'http://dalme.localhost:8000'
    # should be: (after we figure out ida domain)
    # BASE_URL = 'http://ida.localhost:8000' if IS_DEV else 'https://documentaryarchaeology.net'

    API_URL = f'{BASE_URL}/api'
    DAM_URL = 'https://dam.dalme.org'
    URL_PROTOCOL = 'http://' if IS_DEV else 'https://'
    URL_PORT = ':8000' if IS_DEV else ''

    # list of settings values to make available in templates
    INCLUDE_IN_TEMPLATETAG = ['BASE_URL', 'API_URL', 'DAM_URL', 'PUBLIC_URL', 'WAGTAILADMIN_BASE_URL']

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
        bug. It doesn't look like the authors have even considered that anyone
        would use an enum as a setting at this point, as they are a relatively
        new language feature. This all being the case, we can just wrap TENANTS
        in `pristinemethod` here which means that it doesn't undergo the
        `callable` check (which is skipped for `pristinemethod`) which would
        otherwise break startup.

        The expense is that we actually have to call `settings.TENANTS()` in
        the app whenever we need it. We could just make TENANTS a dict to avoid
        this but I prefer to pass around a value with the full typing of a
        struct/enum so we can just pay that price until enums are first-class
        citizens in django-configurations.

        See below for details:

          - https://docs.python.org/3/howto/enum.html
          - https://github.com/jazzband/django-configurations/blob/cad6dcb7f00c26702e5c5305901712409b94c848/configurations/importer.py#L163

        For adding Tenants to an existing deployment update the tenant data
        provided in the environment and run the mangement command
        'ensure_tenants'. This doesn't need to be done manually, the command
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

    ALLOWED_HOSTS = [
        'dalme.localhost',
        'globalpharmacopeias.localhost',
    ]

    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOW_CREDENTIALS = True
    CORS_ALLOWED_ORIGINS = [
        'http://ida.localhost:8000',
        'http://dalme.localhost:8000',
        'http://globalpharmacopeias.localhost:8000',
        'http://localhost:8888',
    ]

    CSRF_COOKIE_SECURE = False
    CSRF_TRUSTED_ORIGINS = [
        'http://ida.localhost:8000',
        'http://dalme.localhost:8000',
        'http://globalpharmacopeias.localhost:8000',
        'http://localhost:8888',
    ]
    SESSION_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
    SECRET_KEY = 'django-development-environment-insecure-secret-key'

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
            'NAME': os.environ['DAM_DB_NAME'],
            'USER': os.environ['DAM_DB_USER'],
            'PASSWORD': os.environ['DAM_DB_PASSWORD'],
            'HOST': os.environ['DAM_DB_HOST'],
            'PORT': os.environ.get('DAM_PORT', 3306),
        },
    }

    DAM_API_USER = os.environ.get('DAM_API_USER')
    DAM_API_KEY = os.environ.get('DAM_API_KEY')

    @property
    def OAUTH2_PROVIDER(self):  # noqa: N802
        """Configure OAuth and OIDC."""
        with open(os.environ['OIDC_RSA_PRIVATE_KEY']) as f:
            return {
                'ACCESS_TOKEN_EXPIRE_SECONDS': self.OAUTH2_ACCESS_TOKEN_EXPIRY,
                'ALLOWED_REDIRECT_URI_SCHEMES': ['http'],
                'OAUTH2_VALIDATOR_CLASS': 'ida.auth.IDAOAuth2Validator',
                'OIDC_ENABLED': True,
                'OIDC_RP_INITIATED_LOGOUT_ENABLED': True,
                'OIDC_RP_INITIATED_LOGOUT_ALWAYS_PROMPT': False,
                'OIDC_RSA_PRIVATE_KEY': f.read(),
                'SCOPES': {
                    'read': 'Read scope',
                    'write': 'Write scope',
                    'groups': 'Auth groups scopes',
                    'openid': 'OpenID Connect scope',
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
            'hosts': os.environ.get('ELASTICSEARCH_ENDPOINT', 'ida.es:9200'),
        },
    }

    # Jupyter notebook setup
    SHELL_PLUS = 'ipython'
    SHELL_PLUS_PRINT_SQL = True
    NOTEBOOK_ARGUMENTS = [
        '--ip',
        '0.0.0.0',
        '--port',
        '8888',
        '--allow-root',
        '--no-browser',
    ]
    IPYTHON_ARGUMENTS = [
        '--ext',
        'django_extensions.management.notebook_extension',
        '--debug',
    ]
    IPYTHON_KERNEL_DISPLAY_NAME = 'Django Shell-Plus'
    SHELL_PLUS_POST_IMPORTS = [  # extra things to import in notebook
        ('module1.submodule', ('func1', 'func2', 'class1', 'etc')),
        ('module2.submodule', ('func1', 'func2', 'class1', 'etc')),
    ]
    os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'


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
                'PORT': os.environ.get('POSTGRES_PORT', 5432),
            },
            'dam': {
                'ENGINE': 'django.db.backends.mysql',
                'NAME': os.environ['DAM_DB_NAME'],
                'USER': os.environ['DAM_DB_USER'],
                'PASSWORD': os.environ['DAM_DB_PASSWORD'],
                'HOST': os.environ['DAM_DB_HOST'],
                'PORT': os.environ.get('DAM_PORT', 3306),
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
    def OAUTH2_PROVIDER(self):  # noqa: N802
        """Configure OAuth and OIDC."""
        return {
            'ACCESS_TOKEN_EXPIRE_SECONDS': self.OAUTH2_ACCESS_TOKEN_EXPIRY,
            'ALLOWED_REDIRECT_URI_SCHEMES': ['https'],
            'OAUTH2_VALIDATOR_CLASS': 'ida.auth.IDAOAuth2Validator',
            'OIDC_ENABLED': True,
            'OIDC_RP_INITIATED_LOGOUT_ENABLED': True,
            'OIDC_RP_INITIATED_LOGOUT_ALWAYS_PROMPT': False,
            'OIDC_RSA_PRIVATE_KEY': os.environ['OIDC_RSA_PRIVATE_KEY'],
            'SCOPES': {
                'read': 'Read scope',
                'write': 'Write scope',
                'groups': 'Auth groups scopes',
                'openid': 'OpenID Connect scope',
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
    # TODO: tenantize?
    DEFAULT_FROM_EMAIL = 'DALME <mail@dalme.org>'

    SHOW_PUBLIC_IF_NO_TENANT_FOUND = False

    # https://docs.djangoproject.com/en/4.2/ref/settings/#storages
    STORAGES = {
        'default': {
            'BACKEND': 'ida.storage_backends.MediaStorage',
        },
        'staticfiles': {
            'BACKEND': 'ida.storage_backends.StaticStorage',
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
