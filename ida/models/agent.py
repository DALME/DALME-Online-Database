"""Agent-related models."""

from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import IDAUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Agent(IDAUuid):
    """Stores information about agents."""

    PERSON = 1
    ORGANIZATION = 2
    AGENT_TYPES = (
        (PERSON, 'Person'),
        (ORGANIZATION, 'Organization'),
    )

    name = models.CharField(max_length=255)
    agent_type = models.IntegerField(choices=AGENT_TYPES)
    attributes = GenericRelation('ida.Attribute')
    instances = GenericRelation('ida.EntityPhrase')
    comments = GenericRelation('ida.Comment')
    tags = GenericRelation('ida.Tag')
    relationships_as_source = GenericRelation(
        'ida.Relationship',
        content_type_field='source_content_type',
        object_id_field='source_object_id',
    )
    relationships_as_target = GenericRelation(
        'ida.Relationship',
        content_type_field='target_content_type',
        object_id_field='target_object_id',
    )


class Organization(Agent):
    """Stores information about organizations."""

    short_name = models.CharField(max_length=55)
    location = models.ForeignKey('ida.Location', on_delete=models.PROTECT, null=True)


class Person(Agent):
    """Stores information about people."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='person_record',
        null=True,
    )

    def __str__(self):
        return self.name
