"""Attachment model."""

import mimetypes
import pathlib

from django.db import models
from django.db.models import options

from ida.models.templates import OwnedMixin, TrackedMixin, UuidMixin
from ida.models.tenant_scoped import ScopedBase

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Attachment(ScopedBase, UuidMixin, TrackedMixin, OwnedMixin):
    """Stores attachment information."""

    filefield = models.FileField(upload_to='attachments/%Y/%m/', max_length=255)
    filetype = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.filefield.name

    @property
    def filename(self):
        """Return file name."""
        return pathlib.Path(self.filefield.name).name

    @property
    def source(self):
        """Return file S3 url."""
        # TODO: generalize this and use variable to compose url
        return f'https://dalme-app-media.s3.amazonaws.com/media/{self.filefield}'

    def extension(self):
        """Return file extension."""
        return pathlib.Path(self.filefield.name).suffix

    def save(self, *args, **kwargs):
        """Save record."""
        mtype, encoding = mimetypes.guess_type(str(self.filefield).split('/').pop(-1))
        self.filetype = mtype
        super().save(*args, **kwargs)
