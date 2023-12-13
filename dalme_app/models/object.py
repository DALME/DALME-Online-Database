"""Model object data."""
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import dalmeUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Object(dalmeUuid):
    """Stores object information."""

    concept = models.ForeignKey('Concept', db_index=True, on_delete=models.CASCADE)
    instances = GenericRelation('EntityPhrase')
    tags = GenericRelation('Tag')


class ObjectAttribute(dalmeUuid):
    """Stores attribute concepts for objects."""

    obj = models.ForeignKey('Object', db_index=True, on_delete=models.CASCADE)
    attribute_concept = models.ForeignKey('Concept', db_index=True, on_delete=models.CASCADE)
