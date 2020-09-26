from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from dalme_app.models._templates import dalmeUuid
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class Token(dalmeUuid):
    object_phrase_id = models.ForeignKey('Entity_phrase', to_field='id', db_index=True, on_delete=models.CASCADE)
    wordform_id = models.ForeignKey('Wordform', to_field='id', db_index=True, on_delete=models.PROTECT)
    raw_token = models.CharField(max_length=255)
    clean_token = models.CharField(max_length=55)
    order = models.IntegerField(db_index=True)
    flags = models.CharField(max_length=10)
    tags = GenericRelation('Tag')

    def __str__(self):
        return self.raw_token
