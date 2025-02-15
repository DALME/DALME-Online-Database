"""Management command to reset db sequences for a migration deploy."""

import os

import structlog
from StringIO import StringIO

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection

os.environ['DJANGO_COLORS'] = 'nocolor'

logger = structlog.get_logger(__name__)


class Command(BaseCommand):
    """Define the reset_sequences command."""

    def handle(self, *args, **options):  # noqa: ARG002
        """Execute the SQL to reset db table sequences."""
        commands = StringIO()
        cursor = connection.cursor()

        for app in apps.get_app_configs():
            call_command('sqlsequencereset', app.label, stdout=commands)
            logger.info('Resetting sequences for app: %s', app=app.label)

        cursor.execute(commands.getvalue())
