"""Objects model."""

from django.db import models
from django.db.models import options

from ida.models.utils import AttestationMixin, TaggingMixin, TrackingMixin, UuidMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Object(UuidMixin, TrackingMixin, AttestationMixin, TaggingMixin):
    """Stores object information."""

    concept = models.ForeignKey('ida.Concept', db_index=True, on_delete=models.CASCADE)


class ObjectAttribute(UuidMixin, TrackingMixin):
    """Stores attribute concepts for objects."""

    obj = models.ForeignKey('ida.Object', db_index=True, on_delete=models.CASCADE)
    attribute_concept = models.ForeignKey('ida.Concept', db_index=True, on_delete=models.CASCADE)
