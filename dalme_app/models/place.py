from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from dalme_app.models._templates import dalmeUuid
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class Place(dalmeUuid):
    standard_name = models.CharField(max_length=255)
    type = models.IntegerField(db_index=True, null=True)
    attributes = GenericRelation('Attribute')
    instances = GenericRelation('Entity_phrase')
    locale = models.ForeignKey('LocaleReference', on_delete=models.SET_NULL, null=True)
    notes = models.TextField(blank=True)
    tags = GenericRelation('Tag')
