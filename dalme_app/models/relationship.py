from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import options

from dalme_app.models.templates import dalmeUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Relationship(dalmeUuid):
    """Stores information about relationships between resources."""

    source_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        related_name='relationship_sources',
    )
    source_object_id = models.UUIDField(null=True, db_index=True)
    source_object = GenericForeignKey('source_content_type', 'source_object_id')
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        related_name='relationship_targets',
    )
    target_object_id = models.UUIDField(null=True, db_index=True)
    target_object = GenericForeignKey('target_content_type', 'target_object_id')
    attributes = GenericRelation('Attribute')
    scope = models.ForeignKey('Scope', on_delete=models.CASCADE, null=True)
    notes = models.TextField(blank=True)
