from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from dalme_app.models._templates import dalmeUuid
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class Object(dalmeUuid):
    concept = models.ForeignKey('Concept', db_index=True, on_delete=models.CASCADE)
    instances = GenericRelation('Entity_phrase')
    tags = GenericRelation('Tag')


class Object_attribute(dalmeUuid):
    object = models.ForeignKey('Object', db_index=True, on_delete=models.CASCADE)
    attribute_concept = models.ForeignKey('Concept', db_index=True, on_delete=models.CASCADE)
