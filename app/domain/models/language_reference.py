"""Language reference model."""

from django.db import models
from django.db.models import options

from domain.models.abstract import TrackingMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db', 'attribute_matching_fields')


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
        attribute_matching_fields = ['name', 'parent']

    def __str__(self):
        return self.name

    def get_url(self):
        """Return url for instance."""
        return f'/languages/{self.id}'
