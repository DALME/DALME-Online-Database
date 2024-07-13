"""Relationship-related models."""

from django.contrib.contenttypes.fields import (
    GenericForeignKey,
)
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import options

from ida.models.abstract import TrackingMixin, UuidMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class RelationshipType(TrackingMixin):
    """Stores relationship type definitions."""

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55, unique=True)
    description = models.TextField()
    source = models.CharField(max_length=255, blank=True)
    is_directed = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Relationship(UuidMixin, TrackingMixin):
    """Stores information about relationships between resources."""

    source = GenericForeignKey('source_content_type', 'source_object_id')
    target = GenericForeignKey('target_content_type', 'target_object_id')
    source_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        related_name='rel_sources',
    )
    source_object_id = models.CharField(max_length=36, db_index=True)
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        related_name='rel_targets',
    )
    target_object_id = models.CharField(max_length=36, db_index=True)
    rel_type = models.ForeignKey(
        'ida.RelationshipType',
        db_index=True,
        on_delete=models.CASCADE,
        db_column='rel_type',
        related_name='relationships',
    )
    scopes = models.ManyToManyField('ida.Scope', db_index=True)
    notes = models.TextField(blank=True)
