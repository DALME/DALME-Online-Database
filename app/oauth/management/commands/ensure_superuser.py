"""Utility management command for ecs to create a superuser at deploy-time."""

import os

import structlog

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

logger = structlog.get_logger(__name__)

DEPLOY_ENVS = {'staging', 'production'}


User = get_user_model()


class Command(BaseCommand):
    """Define the ensure_superuser command."""

    help = 'Create a superuser non-interactively.'

    def handle(self, *args, **options) -> None:  # noqa: ARG002
        """Create a superuser using credentials from the environment.

        This command only runs automated as part of an ecs task definition.
        Developers make a superuser with `create_superuser` instead.

        We also take care to ensure that the superuser record stays up-to-date
        with its corresponding secret that might at some point get rotated by
        terraform apply.

        """
        if settings.ENV not in DEPLOY_ENVS:
            msg = 'ensure_superuser runs only in deployments: use create_superuser in development'
            raise CommandError(msg)

        try:
            username = os.environ['ADMIN_USERNAME']
            password = os.environ['ADMIN_PASSWORD']
        except KeyError:
            msg = 'Missing admin user credentials in environment'
            logger.exception(msg)
            raise

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            User.objects.create_user(
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
