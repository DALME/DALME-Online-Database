import os

from .common import *  # noqa: F403

# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# CSRF
CSRF_COOKIE_SAMESITE = 'None'
CSRF_COOKIE_HTTPONLY = False

# Session
USE_HTTPS = True
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_HTTPONLY = False

# Static and media file configuration
COMPRESS_ENABLED = False
COMPRESS_OFFLINE = False

# Cache and logging
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/var/tmp/django_cache',
    },
}

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
else:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'file': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filename': '/var/log/django/dalme_app.log',
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
