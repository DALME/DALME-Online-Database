from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from dalme_app.models._templates import dalmeUuid
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class Headword(dalmeUuid):
    word = models.CharField(max_length=55)
    full_lemma = models.CharField(max_length=255)
    concept_id = models.ForeignKey('Concept', to_field='id', db_index=True, on_delete=models.PROTECT)
    tags = GenericRelation('Tag')

    def __str__(self):
        return self.word
