"""WSGI entrypoint for IDA application."""

import os

SETTINGS_MAP = {
    'ci': 'CI',
    'development': 'Development',
    'production': 'Production',
    'staging': 'Staging',
}

configuration = SETTINGS_MAP[os.environ['ENV']]

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ida.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', configuration)

from configurations.wsgi import get_wsgi_application  # noqa: E402

application = get_wsgi_application()
