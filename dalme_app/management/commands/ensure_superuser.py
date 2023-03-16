"""Utility management command for ecs to create a superuser at deploy-time."""
import os

import structlog

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

logger = structlog.get_logger(__name__)


class Command(BaseCommand):
    """Define the ensure_superuser command."""

    help = 'Create a superuser non-interactively.'  # noqa: A003

    def handle(self, *args, **options):  # noqa: ARG002
        """Create a superuser using credentials from the environment.

        This command only runs automated as part of an ecs task definition.

        We also take care to ensure that the superuser record stays up-to-date
        with its corresponding secret that might at some point get rotated by
        terraform apply.

        """
        try:
            username = os.environ['ADMIN_USERNAME']
            password = os.environ['ADMIN_PASSWORD']
        except KeyError:
            logger.exception('Missing admin user credentials in environment')
            raise

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            User.objects.create(
                username=username,
                password=password,
                is_superuser=True,
            )
            logger.info('Created superuser', user=username)
        else:
            user.set_password(password)
            user.is_superuser = True
            user.save()
            logger.info('Refreshed password for superuser', user=username)
