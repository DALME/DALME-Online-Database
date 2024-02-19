"""Model token data."""
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import dalmeUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Token(dalmeUuid):
    object_phrase = models.ForeignKey('ida.EntityPhrase', db_index=True, on_delete=models.CASCADE)
    wordform = models.ForeignKey('ida.Wordform', db_index=True, on_delete=models.PROTECT)
    raw_token = models.CharField(max_length=255)
    clean_token = models.CharField(max_length=55)
    order = models.IntegerField(db_index=True)
    flags = models.CharField(max_length=10)
    tags = GenericRelation('dalme_app.Tag')

    def __str__(self):
        return self.raw_token
