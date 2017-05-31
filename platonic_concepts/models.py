from django.db import models

from uuid import uuid4

def make_uuid():
    the_id = uuid4().hex
    return the_id

class PlatonicConcept(models.Model):
    _id = models.CharField(
        max_length=36,
        db_column='id',
        primary_key=True,
        default=make_uuid,
        unique=True
    )
    term = models.CharField(max_length=255, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    creation_username = models.CharField(max_length=255, null=True, blank=True)
    creation_timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modification_username = models.CharField(max_length=255, null=True, blank=True)
    modification_timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return self.term

class Relationship(models.Model):
    _id = models.CharField(
        max_length=36,
        db_column='id',
        primary_key=True,
        default=make_uuid,
        unique=True
    )
    source = models.ForeignKey(PlatonicConcept, related_name='source')
    target = models.ForeignKey(PlatonicConcept, related_name='target')
    relationship = models.CharField(max_length=36)
    def __str__(self):
        representation = "{} - {} -> {}".format(self.source,self.relationship,self.target)
        return representation
