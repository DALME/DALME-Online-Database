"""Objects model."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import TrackedMixin, UuidMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Object(UuidMixin, TrackedMixin):
    """Stores object information."""

    concept = models.ForeignKey('ida.Concept', db_index=True, on_delete=models.CASCADE)
    instances = GenericRelation('ida.EntityPhrase')
    tags = GenericRelation('ida.Tag')


class ObjectAttribute(UuidMixin, TrackedMixin):
    """Stores attribute concepts for objects."""

    obj = models.ForeignKey('ida.Object', db_index=True, on_delete=models.CASCADE)
    attribute_concept = models.ForeignKey('ida.Concept', db_index=True, on_delete=models.CASCADE)
