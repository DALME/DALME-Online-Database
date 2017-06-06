from django.db import models

from .modelTemplates import DalmeBaseModel

from uuid import uuid4

def make_uuid():
    the_id = uuid4().hex
    return the_id

class PlatonicConcept(DalmeBaseModel):
    term = models.CharField(max_length=255, null=True, blank=True)
    getty_term = models.CharField(max_length=255, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.term

class Relationship(DalmeBaseModel):
    source = models.ForeignKey(PlatonicConcept, related_name='source')
    target = models.ForeignKey(PlatonicConcept, related_name='target')
    relationship = models.CharField(max_length=36)
    def __str__(self):
        representation = "{} - {} -> {}".format(self.source,self.relationship,self.target)
        return representation

class SourceType(DalmeBaseModel):
    comments = models.TextField(null=True, blank=True)
    type_csl = models.CharField(max_length=255, null=True, blank=True)
    type_zotero = models.CharField(max_length=255, null=True, blank=True)
    dropdown_content = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        if self.type_csl:
            return self.type_csl
        elif self.type_zotero:
            return self.type_zotero
        else:
            return self.dropdown_content

class SourceAttributeType(DalmeBaseModel):
    type_dublin_core = models.CharField(max_length=255, null=True, blank=True)
    type_csl = models.CharField(max_length=255, null=True, blank=True)
    type_zotero = models.CharField(max_length=255, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    dropdown_content = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.dropdown_content

class Source(DalmeBaseModel):
    source_type = models.ForeignKey(SourceType)
    parent_source = models.ForeignKey("self", related_name='source_parent', null=True, blank=True)
    dropdown_content = models.CharField(max_length=255, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    def __str__(self):
        return self.dropdown_content

class SourceAttribute(DalmeBaseModel):
    source = models.ForeignKey(Source)
    type = models.ForeignKey(SourceAttributeType)
    content = models.CharField(max_length=255, null=True, blank=True)
    comments = models.TextField(null=True, blank=True)
    def __str__(self):
        representation = "{}: {}".format(self.type,self.content)
        return representation
