import requests

from .common import *  # noqa: F403


def get_ec2_instance_ip():
    """Try to obtain the IP address of the current EC2 instance in AWS."""
    try:
        ip = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4', timeout=0.01).text
    except requests.exceptions.ConnectionError:
        return None
    else:
        return ip


# Hosting
ALLOWED_HOSTS.append(get_ec2_instance_ip())  # noqa: F405

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = 'DALME <mail@dalme.org>'

# Static and media file storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True

# Cache and logging
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    },
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
            'filename': '/opt/python/log/dalme_app.log',
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
            'propagate': False,
        },
    },
}
