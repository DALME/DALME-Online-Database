#!/usr/bin/env python
"""Django command entrypoint."""
import os
import sys

SETTINGS_MAP = {
    'ci': 'CI',
    'development': 'Development',
    'production': 'Production',
    'staging': 'Staging',
}

if __name__ == '__main__':
    configuration = SETTINGS_MAP[os.environ['ENV']]

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dalme.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', configuration)

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)
