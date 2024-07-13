"""Mixin that allows model instances to serve as source/target in relationships."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models


class RelationshipMixin(models.Model):
    relationships_as_source = GenericRelation(
        'ida.Relationship',
        content_type_field='source_content_type',
        object_id_field='source_object_id',
        related_query_name='%(app_label)s_%(class)s_source',
    )
    relationships_as_target = GenericRelation(
        'ida.Relationship',
        content_type_field='target_content_type',
        object_id_field='target_object_id',
        related_query_name='%(app_label)s_%(class)s_target',
    )

    class Meta:
        abstract = True
