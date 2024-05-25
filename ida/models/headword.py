"""Headword model."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import TrackedMixin, UuidMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Headword(UuidMixin, TrackedMixin):
    """Stores head word information."""

    word = models.CharField(max_length=55)
    full_lemma = models.CharField(max_length=255)
    concept = models.ForeignKey('ida.Concept', db_index=True, on_delete=models.PROTECT)
    tags = GenericRelation('ida.Tag')

    def __str__(self):
        return self.word
