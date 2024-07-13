"""Concepts model."""

from django.db import models
from django.db.models import options

from ida.models.abstract import TrackingMixin, UuidMixin
from ida.models.tag import TagMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Concept(UuidMixin, TrackingMixin, TagMixin):
    getty_id = models.IntegerField(db_index=True)
