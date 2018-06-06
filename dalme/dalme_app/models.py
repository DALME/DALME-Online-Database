"""
This file defines all of the models used in the application. These models are
used to create database entries, and can be used in other functions to access
and iterate through data in the database without writing SQL statements.
"""

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

import uuid

from .modelTemplates import dalmeBasic, dalmeUuid, dalmeIntid

#function for creating UUIDs - not used, but migrations won't work without it
def make_uuid():
    the_id = uuid.uuid4().hex
    return the_id

#one-to-one extension of user model to accomodate full_name (used by WP-OAuth)
class Profile(models.Model):
    DAM_USERGROUPS = (
        (1, 'Administrator'),
        (2, 'General User'),
        (3, 'Super Admin'),
        (4, 'Archivist')
    )

    WIKI_GROUPS = (
        ('users', 'User'),
        ('administrator', 'Administrator'),
        ('bureaucrat', 'Bureaucrat')
    )

    WP_ROLE = (
        ('a:1:{s:13:"administrator";b:1;}', 'Administrator'),
        ('a:1:{s:6:"editor";b:1;}', 'Editor'),
        ('a:1:{s:6:"author";b:1;}', 'Author'),
        ('a:1:{s:11:"contributor";b:1;}', 'Contributor'),
        ('a:1:{s:10:"subscriber";b:1;}', 'Subscriber')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, blank=True)
    dam_userid = models.IntegerField(null=True)
    dam_usergroup = models.IntegerField(choices=DAM_USERGROUPS, null=True)
    wiki_userid = models.IntegerField(null=True)
    wiki_username = models.CharField(max_length=50, null=True)
    wiki_groups = models.CharField(max_length=255, null=True)
    wp_userid = models.IntegerField(null=True)
    wp_role = models.CharField(max_length=50, null=True, choices=WP_ROLE)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

#DALME data store
class Agents(dalmeUuid):
    type = models.IntegerField()

class Attribute_types(dalmeIntid):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.TextField()
    data_type = models.CharField(max_length=15)

class Attributes(dalmeUuid):
    attribute_type = models.IntegerField(db_index=True)
    content_id = models.UUIDField(db_index=True)

class Attributes_DATE(dalmeBasic):
    attribute_id = models.ForeignKey('Attributes', to_field='id', db_index=True, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    value_day = models.IntegerField()
    value_month = models.IntegerField()
    value_year = models.IntegerField()

class Attributes_DBR(dalmeBasic):
    attribute_id = models.ForeignKey('Attributes', to_field='id', db_index=True, on_delete=models.CASCADE)
    value = models.CharField(max_length=32)

class Attributes_INT(dalmeBasic):
    attribute_id = models.ForeignKey('Attributes', to_field='id', db_index=True, on_delete=models.CASCADE)
    value = models.IntegerField()

class Attributes_STR(dalmeBasic):
    attribute_id = models.ForeignKey('Attributes', to_field='id', db_index=True, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

class Attributes_TXT(dalmeBasic):
    attribute_id = models.ForeignKey('Attributes', to_field='id', db_index=True, on_delete=models.CASCADE)
    value = models.TextField()

class Concepts(dalmeUuid):
    getty_id = models.IntegerField(db_index=True)

class Content_classes(dalmeIntid):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.TextField()

class Content_types(dalmeIntid):
    content_class = models.IntegerField()
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.TextField()

class Content_types_x_attribute_types(dalmeBasic):
    content_type = models.ForeignKey('Content_types', to_field='id', db_index=True, on_delete=models.CASCADE)
    attribute_type = models.ForeignKey('Attribute_types', to_field='id', db_index=True, on_delete=models.PROTECT)
    order = models.IntegerField(db_index=True)

class Headwords(dalmeUuid):
    word = models.CharField(max_length=55)
    full_lemma = models.CharField(max_length=255)
    concept_id = models.ForeignKey('Concepts', to_field='id', db_index=True, on_delete=models.PROTECT)

class Objects(dalmeUuid):
    concept_id = models.UUIDField(db_index=True)
    object_phrase_id = models.ForeignKey('Object_phrases', to_field='id', db_index=True, on_delete=models.CASCADE)

class Object_attributes(dalmeBasic):
    object_id = models.ForeignKey('Objects', to_field='id', db_index=True, on_delete=models.CASCADE)
    concept_id = models.UUIDField(db_index=True)

class Places(dalmeUuid):
    type = models.IntegerField(db_index=True)

class Sources(dalmeUuid):
    type = models.IntegerField(db_index=True)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    parent_source = models.UUIDField(null=True, default=None, db_index=True)
    is_inventory = models.BooleanField(default=False, db_index=True)

class Pages(dalmeUuid):
    source_id = models.ForeignKey('Sources', to_field='id', db_index=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=55)
    dam_id = models.IntegerField(db_index=True)
    order = models.IntegerField(db_index=True)

class Transcriptions(dalmeUuid):
    source_id = models.ForeignKey('Sources', to_field='id', db_index=True, on_delete=models.CASCADE)
    transcription = models.TextField()

class Identity_phrases(dalmeUuid):
    transcription_id = models.ForeignKey('Transcriptions', to_field='id', db_index=True, on_delete=models.CASCADE)
    phrase = models.TextField()

class Object_phrases(dalmeUuid):
    transcription_id = models.ForeignKey('Transcriptions', to_field='id', db_index=True, on_delete=models.CASCADE)
    phrase = models.TextField()

class Word_forms(dalmeUuid):
    normalized_form = models.CharField(max_length=55)
    pos = models.CharField(max_length=255)
    headword_id = models.ForeignKey('Headwords', to_field='id', db_index=True, on_delete=models.PROTECT)

class Tokens(dalmeUuid):
    object_phrase_id = models.ForeignKey('Object_phrases', to_field='id', db_index=True, on_delete=models.CASCADE)
    word_form_id = models.ForeignKey('Word_forms', to_field='id', db_index=True, on_delete=models.PROTECT)
    raw_token = models.CharField(max_length=255)
    clean_token = models.CharField(max_length=55)
    order = models.IntegerField(db_index=True)
    flags = models.CharField(max_length=10)

class Identity_phrases_x_entities(dalmeBasic):
    identity_phrase_id = models.ForeignKey('Identity_phrases', to_field='id', db_index=True, on_delete=models.CASCADE)
    entity_id = models.UUIDField(db_index=True)

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
    e_code = models.IntegerField(primary_key=True, unique=True, db_index=True)
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
