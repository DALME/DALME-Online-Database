"""Token model."""

from django.db import models
from django.db.models import options

from app.abstract import TrackingMixin, UuidMixin
from domain.models.tag import TagMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Token(UuidMixin, TrackingMixin, TagMixin):
    object_phrase = models.ForeignKey('domain.EntityPhrase', db_index=True, on_delete=models.CASCADE)
    wordform = models.ForeignKey('domain.Wordform', db_index=True, on_delete=models.PROTECT)
    raw_token = models.CharField(max_length=255)
    clean_token = models.CharField(max_length=55)
    order = models.IntegerField(db_index=True)
    flags = models.CharField(max_length=10)

    def __str__(self):
        return self.raw_token
