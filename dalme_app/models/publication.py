from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from dalme_app.models.templates import dalmeUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Publication(dalmeUuid):
    """Stores information about publications."""

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    attributes = GenericRelation('Attribute', related_query_name='publications')
    permissions = GenericRelation('Permission', related_query_name='publication')
    tags = GenericRelation('Tag')
    comments = GenericRelation('Comment')
