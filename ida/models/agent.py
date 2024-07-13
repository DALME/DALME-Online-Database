"""Agent-related models."""

from django.conf import settings
from django.db import models
from django.db.models import options

from ida.models.abstract import TrackingMixin, UuidMixin
from ida.models.attribute import AttributeMixin
from ida.models.comment import CommentMixin
from ida.models.entity import AttestationMixin
from ida.models.relationship import RelationshipMixin
from ida.models.tag import TagMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db', 'attribute_matching_fields')


class Agent(
    UuidMixin,
    TrackingMixin,
    AttributeMixin,
    CommentMixin,
    TagMixin,
    RelationshipMixin,
    AttestationMixin,
):
    """Stores information about agents."""

    PERSON = 1
    ORGANIZATION = 2
    AGENT_TYPES = (
        (PERSON, 'Person'),
        (ORGANIZATION, 'Organization'),
    )

    name = models.CharField(max_length=255)
    agent_type = models.IntegerField(choices=AGENT_TYPES)


class Organization(Agent):
    """Stores information about organizations."""

    short_name = models.CharField(max_length=55)
    location = models.ForeignKey('ida.Location', on_delete=models.PROTECT, null=True)

    class Meta:
        attribute_matching_fields = ['name', 'label']


class Person(Agent):
    """Stores information about people."""

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name='person_record',
        null=True,
    )

    class Meta:
        attribute_matching_fields = ['name', 'user']

    def __str__(self):
        return self.name
