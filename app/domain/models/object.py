"""Objects model."""

from django.db import models
from django.db.models import options

from app.abstract import TrackingMixin, UuidMixin
from domain.models.entity import AttestationMixin
from domain.models.tag import TagMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Object(UuidMixin, TrackingMixin, AttestationMixin, TagMixin):
    """Stores object information."""

    concept = models.ForeignKey('domain.Concept', db_index=True, on_delete=models.CASCADE)


class ObjectAttribute(UuidMixin, TrackingMixin):
    """Stores attribute concepts for objects."""

    obj = models.ForeignKey('domain.Object', db_index=True, on_delete=models.CASCADE)
    attribute_concept = models.ForeignKey('domain.Concept', db_index=True, on_delete=models.CASCADE)
