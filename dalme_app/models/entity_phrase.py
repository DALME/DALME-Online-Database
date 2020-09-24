from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from dalme_app.models._templates import dalmeUuid
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class Entity_phrase(dalmeUuid):
    AGENT = 1
    OBJECT = 2
    PLACE = 3
    ENTITY_TYPES = (
        (AGENT, 'Agent'),
        (OBJECT, 'Object'),
        (PLACE, 'Place'),
    )

    phrase = models.TextField(blank=True)
    type = models.IntegerField(choices=ENTITY_TYPES)
    transcription_id = models.ForeignKey('Transcription', to_field='id', db_index=True, on_delete=models.CASCADE, related_name='entity_phrases')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.UUIDField(null=True, db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.phrase
