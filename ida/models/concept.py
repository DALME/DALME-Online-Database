"""Concepts model."""

from django.db import models
from django.db.models import options

from ida.models.utils import TaggingMixin, TrackingMixin, UuidMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Concept(UuidMixin, TrackingMixin, TaggingMixin):
    getty_id = models.IntegerField(db_index=True)
