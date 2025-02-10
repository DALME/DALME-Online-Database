"""Entity phrase model."""

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import options

from app.abstract import TrackingMixin, UuidMixin
from domain.models.attribute import AttributeMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class EntityPhrase(UuidMixin, TrackingMixin, AttributeMixin):
    """Stores entity-phrase information."""

    transcription = models.ForeignKey(
        'domain.Transcription',
        to_field='id',
        db_index=True,
        on_delete=models.CASCADE,
        related_name='entity_phrases',
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.UUIDField(null=True, db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')
