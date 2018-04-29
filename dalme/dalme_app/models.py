from django.db import models
from .modelTemplates import dalmeBasic, dalmeUuid, dalmeIntid
import uuid

def make_uuid():
    the_id = uuid.uuid4().hex
    return the_id

class agents(dalmeUuid):
    type = models.IntegerField()

class attribute_types(dalmeIntid):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.TextField()
    data_type = models.CharField(max_length=15)

class attributes(dalmeUuid):
    attribute_type = models.IntegerField()
    content_id = models.CharField(max_length=32)

class attributes_DATE(dalmeBasic):
    attribute_id = models.ForeignKey('attributes', to_field='id', max_length=32)
    value = models.DateField(auto_now=False, auto_now_add=False)
    value_day = models.IntegerField()
    value_month = models.IntegerField()
    value_year = models.IntegerField()

class attributes_DBR(dalmeBasic):
    attribute_id = models.ForeignKey('attributes', to_field='id', max_length=32)
    value = models.CharField(max_length=32)

class attributes_INT(dalmeBasic):
    attribute_id = models.ForeignKey('attributes', to_field='id', max_length=32)
    value = models.IntegerField()

class attributes_STR(dalmeBasic):
    attribute_id = models.ForeignKey('attributes', to_field='id', max_length=32)
    value = models.CharField(max_length=255)

class attributes_TXT(dalmeBasic):
    attribute_id = models.ForeignKey('attributes', to_field='id', max_length=32)
    value = models.TextField()

class concepts(dalmeUuid):
    id = models.CharField(primary_key=True, max_length=32, unique=True)
    getty_id = models.IntegerField()

class content_classes(dalmeIntid):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.TextField()

class content_types(dalmeIntid):
    content_class = models.IntegerField()
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.TextField()

class content_types_x_attribute_types(dalmeBasic):
    content_type = models.ForeignKey('content_types', to_field='id')
    attribute_type = models.ForeignKey('attribute_types', to_field='id')
    order = models.IntegerField()

class headwords(dalmeUuid):
    word = models.CharField(max_length=55)
    full_lemma = models.CharField(max_length=255)
    concept_id = models.ForeignKey('concepts', to_field='id', max_length=32)

class objects(dalmeUuid):
    concept_id = models.CharField(max_length=32)
    object_phrase_id = models.ForeignKey('object_phrases', to_field='id', max_length=32)

class object_attributes(dalmeBasic):
    object_id = models.ForeignKey('objects', to_field='id', max_length=32)
    concept_id = models.CharField(max_length=32)

class places(dalmeUuid):
    type = models.IntegerField()

class sources(dalmeUuid):
    type = models.IntegerField()
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    parent_source = models.CharField(max_length=32)
    is_inventory = models.BooleanField(default=False)

class pages(dalmeUuid):
    source_id = models.ForeignKey('sources', to_field='id', max_length=32)
    name = models.CharField(max_length=55)
    dam_id = models.IntegerField()
    order = models.IntegerField()

class transcriptions(dalmeUuid):
    source_id = models.ForeignKey('sources', to_field='id', max_length=32)
    transcription = models.TextField()

class identity_phrases(dalmeUuid):
    transcription_id = models.ForeignKey('transcriptions', to_field='id', max_length=32)
    phrase = models.TextField()

class object_phrases(dalmeUuid):
    transcription_id = models.ForeignKey('transcriptions', to_field='id', max_length=32)
    phrase = models.TextField()

class word_forms(dalmeUuid):
    normalized_form = models.CharField(max_length=55)
    pos = models.CharField(max_length=255)
    headword_id = models.ForeignKey('headwords', to_field='id', max_length=32)

class tokens(dalmeUuid):
    object_phrase_id = models.ForeignKey('object_phrases', to_field='id', max_length=32)
    word_form_id = models.ForeignKey('word_forms', to_field='id', max_length=32)
    raw_token = models.CharField(max_length=255)
    clean_token = models.CharField(max_length=55)
    order = models.IntegerField()
    flags = models.CharField(max_length=10)

class identity_phrases_x_entities(dalmeBasic):
    identity_phrase_id = models.ForeignKey('identity_phrases', to_field='id', max_length=32)
    entity_id = models.CharField(max_length=32)

#app management models
class error_messages(dalmeBasic):
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

#temporary models for testing parser
class par_inventories(dalmeUuid):
    title = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    series = models.CharField(max_length=16)
    shelf = models.CharField(max_length=32)
    transcriber = models.CharField(max_length=32)

class par_folios(dalmeUuid):
    inv_id = models.ForeignKey('par_inventories', on_delete=models.CASCADE)
    folio_no = models.CharField(max_length=32)
    dam_id = models.IntegerField()

class par_tokens(dalmeUuid):
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

class par_objects(models.Model):
    obj_id = models.IntegerField(primary_key=True, unique=True)
    ont_class = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    terms = models.CharField(max_length=255)
    material = models.CharField(max_length=64)
    room = models.CharField(max_length=64)
