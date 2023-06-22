import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Create superuser."""

    def handle(self):
        """Override handle method."""
        if not User.objects.filter(username="jguillette").exists():
            User.objects.create_superuser(
                os.environ['DJANGO_SUPERUSER_NAME'],
                os.environ['DJANGO_SUPERUSER_EMAIL'],
                os.environ['DJANGO_SUPERUSER_PASSWORD'],
            )
