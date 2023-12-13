"""Model concept data."""
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import dalmeUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Concept(dalmeUuid):
    getty_id = models.IntegerField(db_index=True)
    tags = GenericRelation('Tag')
