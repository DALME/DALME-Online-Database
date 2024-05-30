"""Scope-related models."""

from django.db import models
from django.db.models import options

from ida.models.utils import TrackingMixin, UuidMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class ScopeType(TrackingMixin):
    """Stores scope type definitions."""

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55, unique=True)
    description = models.TextField()
    source = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.name


class Scope(UuidMixin, TrackingMixin):
    """Stores information about scopes."""

    scope_type = models.ForeignKey(
        'ida.ScopeType',
        db_index=True,
        on_delete=models.CASCADE,
        db_column='scope_type',
        related_name='scopes',
    )
    parameters = models.JSONField()
    notes = models.TextField(blank=True)
