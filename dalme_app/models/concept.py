from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from dalme_app.models._templates import dalmeUuid
import django.db.models.options as options

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class Concept(dalmeUuid):
    getty_id = models.IntegerField(db_index=True)
    tags = GenericRelation('Tag')
