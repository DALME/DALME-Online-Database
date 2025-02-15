"""Management command to reset db sequences for a migration deploy."""

import io
import os

import structlog
from psycopg.errors import UndefinedTable

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.db import connection, transaction
from django.db.utils import ProgrammingError

os.environ['DJANGO_COLORS'] = 'nocolor'

logger = structlog.get_logger(__name__)


class Command(BaseCommand):
    """Define the reset_sequences command."""

    def handle(self, *args, **options):  # noqa: ARG002
        """Execute the SQL to reset db table sequences."""
        cursor = connection.cursor()

        for app in apps.get_app_configs():
            command = io.StringIO()
            call_command('sqlsequencereset', app.label, stdout=command)
            logger.info('Resetting sequences for app: %s', app=app.label)

            with transaction.atomic():
                try:
                    cursor.execute(command.getvalue())
                except (ProgrammingError, UndefinedTable):
                    logger.exception('Unable to reset sequence for: %', app=app.label)
