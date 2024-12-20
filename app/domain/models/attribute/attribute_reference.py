"""Attribute reference model."""

from django.db import models
from django.db.models import options

from domain.models.abstract import TrackingMixin, UuidMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class AttributeReference(UuidMixin, TrackingMixin):
    """Stores information about the provenance of attribute definitions."""

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.TextField()
    data_type = models.CharField(max_length=15)
    source = models.CharField(max_length=255)
    term_type = models.CharField(max_length=55, blank=True)
