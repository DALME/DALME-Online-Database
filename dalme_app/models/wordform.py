from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from dalme_app.models._templates import dalmeUuid
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class Wordform(dalmeUuid):
    normalized_form = models.CharField(max_length=55)
    pos = models.CharField(max_length=255)
    headword_id = models.ForeignKey('Headword', to_field='id', db_index=True, on_delete=models.PROTECT)
    tags = GenericRelation('Tag')

    def __str__(self):
        return self.normalized_form
