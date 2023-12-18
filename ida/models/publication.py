"""Model publication data."""
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import dalmeUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Publication(dalmeUuid):
    """Stores information about publications."""

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    attributes = GenericRelation('ida.Attribute', related_query_name='publications')
    permissions = GenericRelation('ida.Permission', related_query_name='publication')
    tags = GenericRelation('dalme_app.Tag')
    comments = GenericRelation('dalme_app.Comment')
