"""Language reference model."""

from django.db import models
from django.db.models import options

from ida.models.utils import TrackingMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class LanguageReference(TrackingMixin):
    """Stores information about languages and dialects."""

    glottocode = models.CharField(max_length=25, unique=True)
    iso6393 = models.CharField(
        max_length=25,
        unique=True,
        null=True,
        blank=True,
        default=None,
    )
    name = models.CharField(max_length=255)
    is_dialect = models.BooleanField(default=False)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_url(self):
        """Return url for instance."""
        return f'/languages/{self.id}'
