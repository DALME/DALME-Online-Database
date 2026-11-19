"""Refuse Django's builtin `createsuperuser`."""

from django.contrib.auth.management.commands.createsuperuser import Command as CreateSuperuser
from django.core.management.base import CommandError


class Command(CreateSuperuser):
    """Shadow the builtin, which leaves a user's names blank.

    The UI rejects a user without a first and last name, so an account made by
    the builtin cannot log in to it. The builtin's arguments are kept, so any
    invocation reaches the refusal rather than an argument error.

    """

    help = 'Not used here: run `create_superuser` instead.'

    def handle(self, *args, **options) -> None:  # noqa: ARG002
        """Refuse, naming the command to run instead."""
        msg = 'createsuperuser leaves the names blank, which the UI rejects: run create_superuser instead'
        raise CommandError(msg)
