"""Model object data."""
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import dalmeUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Object(dalmeUuid):
    """Stores object information."""

    concept = models.ForeignKey('ida.Concept', db_index=True, on_delete=models.CASCADE)
    instances = GenericRelation('ida.EntityPhrase')
    tags = GenericRelation('dalme_app.Tag')


class ObjectAttribute(dalmeUuid):
    """Stores attribute concepts for objects."""

    obj = models.ForeignKey('Object', db_index=True, on_delete=models.CASCADE)
    attribute_concept = models.ForeignKey('ida.Concept', db_index=True, on_delete=models.CASCADE)
