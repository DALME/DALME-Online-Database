from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from dalme_app.models.templates import dalmeUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Agent(dalmeUuid):
    """Stores information about agents."""

    PERSON = 1
    ORGANIZATION = 2
    AGENT_TYPES = (
        (PERSON, 'Person'),
        (ORGANIZATION, 'Organization'),
    )

    standard_name = models.CharField(max_length=255)
    type = models.IntegerField(choices=AGENT_TYPES)
    attributes = GenericRelation('Attribute')
    instances = GenericRelation('EntityPhrase')
    relations = GenericRelation(
        'Relationship',
        content_type_field='source_content_type',
        object_id_field='source_object_id',
    )
    notes = models.TextField(blank=True)
    tags = GenericRelation('Tag')
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='agent',
        null=True,
    )
