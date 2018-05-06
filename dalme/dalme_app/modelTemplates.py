from django.db import models
import uuid

def make_uuid():
    the_id = uuid.uuid4().hex
    return the_id

class dalmeBasic(models.Model):
    creation_username = models.CharField(max_length=255, null=True, blank=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modification_username = models.CharField(max_length=255, null=True, blank=True)
    modification_timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        abstract = True

class dalmeUuid(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    creation_username = models.CharField(max_length=255, null=True, blank=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modification_username = models.CharField(max_length=255, null=True, blank=True)
    modification_timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        abstract = True

class dalmeIntid(models.Model):
    id = models.AutoField(primary_key=True, unique=True, db_index=True)
    creation_username = models.CharField(max_length=255, null=True, blank=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modification_username = models.CharField(max_length=255, null=True, blank=True)
    modification_timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        abstract = True
