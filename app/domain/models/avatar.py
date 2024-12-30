"""Abstract reusable avatar functionality."""

import pathlib

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models


def avatar_file_path(instance, filename):
    """Partition avatar file paths by model."""
    return pathlib.Path(
        settings.AVATARS_LOCATION,
        instance.__class__.__name__.lower(),
        filename,
    ).as_posix()


class AvatarField(models.ImageField):
    """Model field holding an avatar image."""

    def __init__(self, *args, **kwargs):
        """Construct the AvatarField."""
        super().__init__(*args, **kwargs)
        self.upload_to = avatar_file_path
        # we specify Django's default storage model to prevent
        # django-tenants from adding the tenant to the path
        self.storage = FileSystemStorage()


class Avatar(models.Model):
    """Bestow an avatar upon a model."""

    avatar = AvatarField(blank=True, null=True, help_text='Profile image or avatar.')

    class Meta:
        abstract = True

    @property
    def avatar_url(self):
        """Return url to avatar image."""
        return settings.MEDIA_URL + self.avatar.file.path
