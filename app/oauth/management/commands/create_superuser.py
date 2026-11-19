"""Management command to create a superuser for local development."""

import structlog

from django.conf import settings
from django.contrib.auth.management.commands.createsuperuser import Command as CreateSuperuser
from django.core.management.base import CommandError
from django.db import transaction

from oauth.models import User

logger = structlog.get_logger(__name__)

FIRST_NAME = 'Development'
LAST_NAME = 'Superuser'


class Command(CreateSuperuser):
    """Define the create_superuser command."""

    help = 'Create a superuser for local development.'

    def handle(self, *args, **options) -> None:
        """Create a superuser through the builtin's prompts, then name it.

        Deployments get their superuser from `ensure_superuser` instead.

        """
        if settings.ENV != 'development':
            msg = 'create_superuser is for local development only'
            raise CommandError(msg)

        with transaction.atomic():
            super().handle(*args, **options)
            user = User.objects.latest('date_joined')
            user.first_name = FIRST_NAME
            user.last_name = LAST_NAME
            user.full_name = f'{FIRST_NAME} {LAST_NAME}'
            user.save()

        logger.info('Created superuser', username=user.username)
