"""Objects model."""

from django.db import models
from django.db.models import options

from ida.models.abstract import TrackingMixin, UuidMixin
from ida.models.entity import AttestationMixin
from ida.models.tag import TagMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Object(UuidMixin, TrackingMixin, AttestationMixin, TagMixin):
    """Stores object information."""

    concept = models.ForeignKey('ida.Concept', db_index=True, on_delete=models.CASCADE)


class ObjectAttribute(UuidMixin, TrackingMixin):
    """Stores attribute concepts for objects."""

    obj = models.ForeignKey('ida.Object', db_index=True, on_delete=models.CASCADE)
    attribute_concept = models.ForeignKey('ida.Concept', db_index=True, on_delete=models.CASCADE)
