"""Model agent data."""
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import dalmeUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Agent(dalmeUuid):
    """Stores information about agents."""

    PERSON = 1
    ORGANIZATION = 2
    AGENT_TYPES = (
        (PERSON, 'Person'),
        (ORGANIZATION, 'Organization'),
    )

    name = models.CharField(max_length=255)
    agent_type = models.IntegerField(choices=AGENT_TYPES)
    attributes = GenericRelation('dalme_app.Attribute')
    instances = GenericRelation('dalme_app.EntityPhrase')
    comments = GenericRelation('dalme_app.Comment')
    tags = GenericRelation('dalme_app.Tag')


class Organization(Agent):
    """Stores information about organizations."""

    short_name = models.CharField(max_length=55)
    location = models.ForeignKey('dalme_app.Location', on_delete=models.PROTECT, null=True)


class Person(Agent):
    """Stores information about people."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='person_record',
        null=True,
    )

    def __str__(self):
        return self.standard_name
