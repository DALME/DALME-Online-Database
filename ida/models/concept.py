"""Model concept data."""

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models.templates import IDAUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Concept(IDAUuid):
    getty_id = models.IntegerField(db_index=True)
    tags = GenericRelation('ida.Tag')
