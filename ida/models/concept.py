"""Concepts model."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import TrackedMixin, UuidMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Concept(UuidMixin, TrackedMixin):
    getty_id = models.IntegerField(db_index=True)
    tags = GenericRelation('ida.Tag')
