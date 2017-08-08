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

class par_inventories(DalmeBaseModel):
    title = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    series = models.CharField(max_length=16)
    shelf = models.CharField(max_length=32)
    transcriber = models.CharField(max_length=32)

class par_folios(DalmeBaseModel):
    inv_id = models.ForeignKey('par_inventories', on_delete=models.CASCADE)
    folio_no = models.CharField(max_length=32)
    dam_id = models.IntegerField()

class par_tokens(DalmeBaseModel):
    folio_id = models.ForeignKey('par_folios', on_delete=models.CASCADE)
    line_no = models.IntegerField()
    position = models.IntegerField()
    raw_token = models.CharField(max_length=64)
    clean_token = models.CharField(max_length=64)
    norm_token = models.CharField(max_length=64)
    token_type = models.CharField(max_length=32)
    flags = models.CharField(max_length=16, null=True, blank=True)
    span_start = models.IntegerField(null=True, blank=True)
    span_end = models.IntegerField(null=True, blank=True)

class error_messages(models.Model):
    LEVELS = (
        (10, 'DEBUG'),
        (20, 'INFO'),
        (25, 'SUCCESS'),
        (30, 'WARNING'),
        (40, 'ERROR')
    )
    TYPES = (
        (1, 'MODAL'),
        (2, 'NOTIFICATION')
    )
    e_code = models.IntegerField(primary_key=True, unique=True)
    e_level = models.IntegerField(choices=LEVELS)
    e_text = models.TextField()
    e_type = models.IntegerField(choices=TYPES)

class par_objects(models.Model):
    obj_id = models.IntegerField(primary_key=True, unique=True)
    ont_class = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    terms = models.CharField(max_length=255)
    material = models.CharField(max_length=64)
    room = models.CharField(max_length=64)
