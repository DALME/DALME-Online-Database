"""Wordform model."""

from django.db import models
from django.db.models import options

from ida.models.utils import TaggingMixin, TrackingMixin, UuidMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Wordform(UuidMixin, TrackingMixin, TaggingMixin):
    """Stores information about word forms."""

    normalized_form = models.CharField(max_length=55)
    pos = models.CharField(max_length=255)
    headword = models.ForeignKey('ida.Headword', db_index=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.normalized_form
