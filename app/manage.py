#!/usr/bin/env python
"""Django command entrypoint."""

from __future__ import annotations

import os
import sys

# Note, deploy environments need to be represented here so management commands
# can use this procedure.
SETTINGS_MAP = {
    'ci': 'CI',
    'development': 'Development',
    'production': 'Production',
    'staging': 'Staging',
    'test': 'Test',
}

if __name__ == '__main__':
    configuration = SETTINGS_MAP[os.environ['ENV']]

    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', configuration)

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)
