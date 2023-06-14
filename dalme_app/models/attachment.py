import mimetypes
import pathlib

from django.db import models
from django.db.models import options

from dalme_app.models.templates import dalmeOwned, dalmeUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Attachment(dalmeUuid, dalmeOwned):
    """Stores attachment information."""

    file = models.FileField(upload_to='attachments/%Y/%m/')
    type = models.CharField(max_length=255, blank=True)

    @property
    def filename(self):
        """Return file name."""
        return pathlib.Path(self.file.name).name

    def extension(self):
        """Return file extension."""
        return pathlib.Path(self.file.name).suffix

    @property
    def source(self):
        """Return file S3 url."""
        return f'https://dalme-app-media.s3.amazonaws.com/media/{self.file!s}'

    def __str__(self):  # noqa: D105
        return self.file.name

    def save(self, *args, **kwargs):
        """Save record."""
        mtype, encoding = mimetypes.guess_type(str(self.file).split('/').pop(-1))
        self.type = mtype
        super().save(*args, **kwargs)
