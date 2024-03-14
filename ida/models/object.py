"""Model object data."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import IDAUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Object(IDAUuid):
    """Stores object information."""

    concept = models.ForeignKey('ida.Concept', db_index=True, on_delete=models.CASCADE)
    instances = GenericRelation('ida.EntityPhrase')
    tags = GenericRelation('ida.Tag')


class ObjectAttribute(IDAUuid):
    """Stores attribute concepts for objects."""

    obj = models.ForeignKey('ida.Object', db_index=True, on_delete=models.CASCADE)
    attribute_concept = models.ForeignKey('ida.Concept', db_index=True, on_delete=models.CASCADE)
