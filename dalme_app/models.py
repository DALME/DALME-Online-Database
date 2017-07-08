from django.db import models

from .modelTemplates import DalmeBaseModel

from uuid import uuid4

def make_uuid():
    the_id = uuid4().hex
    return the_id

class external_lemmata(DalmeBaseModel):
    """ External Lemmata
        This is the model definition for external lemmata,
        currently it only contains fields for id, add/modify tracking, and a temp field I added so that the migrate tool would stop complaining.
        This is a dummy docstring to test the documentation system.
    """
    temp = models.CharField(max_length=255)


class external_lemma_attributes(DalmeBaseModel):
    subject = models.ForeignKey('external_lemmata', related_name='external_lemma_subject')
    predicate = models.CharField(max_length=32)
    _object = models.CharField(max_length=255)
    def __str__(self):
        representation = "{} -> {} -> {}".format(self.subject,self.predicate,self._object)
        return representation


class phrases(DalmeBaseModel):
    parent_phrase = models.CharField(max_length=36)
    _type = models.CharField(max_length=36)
    platonic_concept = models.CharField(max_length=36)


class source_attributes(DalmeBaseModel):
    subject = models.CharField(max_length=32)
    predicate = models.CharField(max_length=32)
    _object = models.CharField(max_length=255)
    comments = models.TextField(null=True, blank=True)
    def __str__(self):
        representation = "{} -> {} -> {}".format(self.subject,self.predicate,self._object)
        return representation


class sources(DalmeBaseModel):
    temp = models.CharField(max_length=255)


class superlemmata(DalmeBaseModel):
    temp = models.CharField(max_length=255)


class superlemma_components(DalmeBaseModel):
    subject = models.ForeignKey('superlemmata', related_name='superlemma_component_subject')
    predicate = models.CharField(max_length=32)
    _object = models.CharField(max_length=255)
    def __str__(self):
        representation = "{} -> {} -> {}".format(self.subject,self.predicate,self._object)
        return representation


class concepts(DalmeBaseModel):
    temp = models.CharField(max_length=255)


class concept_components(DalmeBaseModel):
    subject = models.ForeignKey('concepts', related_name='concept_component_subject')
    predicate = models.CharField(max_length=32)
    _object = models.CharField(max_length=255)
    def __str__(self):
        representation = "{} -> {} -> {}".format(self.subject,self.predicate,self._object)
        return representation


class inventories(DalmeBaseModel):
    temp = models.CharField(max_length=255)


class inventory_versions(DalmeBaseModel):
    inventory = models.ForeignKey('inventories', related_name='inventory')


class leaves(DalmeBaseModel):
    temp = models.CharField(max_length=255)


class leaf_images(DalmeBaseModel):
    leaf = models.ForeignKey('leaves', related_name='image_leaf')


class lines(DalmeBaseModel):
    leaf = models.ForeignKey('leaves', related_name='line_leaf')
    inventory_version = models.ForeignKey('inventory_versions', related_name='inventory_version')


class tokens(DalmeBaseModel):
    token = models.CharField(max_length=255)
    line = models.ForeignKey('lines', related_name='token_line')
    def __str__(self):
        return self.token


class phrase_parts(DalmeBaseModel):
    token = models.ForeignKey('tokens', related_name='phrase_part_token')
    phrase = models.ForeignKey('phrases', related_name='phrase_part_phrase')


class inventory_attributes(DalmeBaseModel):
    temp = models.CharField(max_length=255)


class predicates(DalmeBaseModel):
    uri = models.CharField(max_length=255)
    def __str__(self):
        return self.uri


class predicate_labels(DalmeBaseModel):
    predicate = models.ForeignKey('predicates', related_name='label_predicate')
    language = models.CharField(max_length=36)
    label = models.CharField(max_length=255)
    def __str__(self):
        representation = "@{}:{}".format(self.language,self.label)
        return representation


class references(DalmeBaseModel):
    foreign_id = models.CharField(max_length=36)
    _type = models.CharField(max_length=36)
    source_id = models.CharField(max_length=36)
    comments = models.TextField(null=True, blank=True)


class repository(DalmeBaseModel):
    temp = models.CharField(max_length=255)


class reference_attributes(DalmeBaseModel):
    subject = models.ForeignKey('references', related_name='reference_attribute_subject')
    predicate = models.CharField(max_length=32)
    _object = models.CharField(max_length=32)
    def __str__(self):
        representation = "{} -> {} -> {}".format(self.subject,self.predicate,self._object)
        return representation


class repository_attributes(DalmeBaseModel):
    subject = models.ForeignKey('references', related_name='repository_attribute_subject')
    predicate = models.CharField(max_length=32)
    _object = models.CharField(max_length=32)
    def __str__(self):
        representation = "{} -> {} -> {}".format(self.subject,self.predicate,self._object)
        return representation
