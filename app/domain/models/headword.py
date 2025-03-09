"""Headword model."""

from django.db import models
from django.db.models import options

from app.abstract import TrackingMixin, UuidMixin
from domain.models.tag import TagMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Headword(UuidMixin, TrackingMixin, TagMixin):
    """Stores head word information."""

    word = models.CharField(max_length=55)
    full_lemma = models.CharField(max_length=255)
    concept = models.ForeignKey('domain.Concept', db_index=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.word
