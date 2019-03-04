"""
This file contains templates for models, used in dalme_app.models. These templates
are used to more easily associate common data points with those models, things like
timestamps and unique IDs.
"""

from django.db import models
from dalme_app.middleware import get_current_user
import uuid

def make_uuid():
    the_id = uuid.uuid4().hex
    return the_id

class dalmeBasic(models.Model):
    """
    Model template with timestamps, but no pre-defined ID
    """
    creation_username = models.CharField(max_length=255, null=True, blank=True, default=get_current_user)
    creation_timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modification_username = models.CharField(max_length=255, null=True, blank=True, default=get_current_user)
    modification_timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)
    def class_name(self):
        return self.__class__.__name__
    class Meta:
        abstract = True

class dalmeUuid(models.Model):
    """
    Model template with a unique ID assigned by `uuid.uuid4`, resulting in a
    long, random identifier.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    creation_username = models.CharField(max_length=255, null=True, blank=True, default=get_current_user)
    creation_timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modification_username = models.CharField(max_length=255, null=True, blank=True, default=get_current_user)
    modification_timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)
    def class_name(self):
        return self.__class__.__name__
    class Meta:
        abstract = True

class dalmeIntid(models.Model):
    """
    Model template with a unique ID assigned as a sequential integer
    """
    id = models.AutoField(primary_key=True, unique=True, db_index=True)
    creation_username = models.CharField(max_length=255, null=True, blank=True, default=get_current_user)
    creation_timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modification_username = models.CharField(max_length=255, null=True, blank=True, default=get_current_user)
    modification_timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)
    def class_name(self):
        return self.__class__.__name__
    class Meta:
        abstract = True
