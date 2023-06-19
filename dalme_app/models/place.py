from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from dalme_app.models.templates import dalmeUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Place(dalmeUuid):
    """Stores place information."""

    standard_name = models.CharField(max_length=255)
    type = models.IntegerField(db_index=True, null=True)  # noqa: A003
    attributes = GenericRelation('Attribute')
    instances = GenericRelation('EntityPhrase')
    locale = models.ForeignKey('LocaleReference', on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    tags = GenericRelation('Tag')
