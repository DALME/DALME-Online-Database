"""Model agent data."""
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

    name = models.CharField(max_length=255)
    agent_type = models.IntegerField(choices=AGENT_TYPES)
    attributes = GenericRelation('Attribute')
    instances = GenericRelation('EntityPhrase')
    comments = GenericRelation('Comment')
    tags = GenericRelation('Tag')


class Organization(Agent):
    """Stores information about organizations."""

    short_name = models.CharField(max_length=55)
    location = models.ForeignKey('Location', on_delete=models.PROTECT, null=True)


class Person(Agent):
    """Stores information about people."""

    user = models.OneToOneField(
        User,
        on_delete=models.SET_NULL,
        related_name='person_record',
        null=True,
    )

    def __str__(self):
        return self.standard_name
