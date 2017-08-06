from django.db import models
from uuid import uuid4

def make_uuid():
    the_id = uuid4().hex
    return the_id

class DalmeBaseModel(models.Model):
    _id = models.CharField(
        max_length=36,
        db_column='id',
        primary_key=True,
        default=make_uuid,
        unique=True
    )
    creation_username = models.CharField(max_length=255, null=True, blank=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modification_username = models.CharField(max_length=255, null=True, blank=True)
    modification_timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        abstract = True
