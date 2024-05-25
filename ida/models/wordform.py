"""Wordform model."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import TrackedMixin, UuidMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Wordform(UuidMixin, TrackedMixin):
    """Stores information about word forms."""

    normalized_form = models.CharField(max_length=55)
    pos = models.CharField(max_length=255)
    headword = models.ForeignKey('ida.Headword', db_index=True, on_delete=models.PROTECT)
    tags = GenericRelation('ida.Tag')

    def __str__(self):
        return self.normalized_form
