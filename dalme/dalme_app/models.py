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
class Agent(dalmeUuid):
    type = models.IntegerField()

class Attribute_type(dalmeIntid):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.TextField()
    data_type = models.CharField(max_length=15)

class Attribute(dalmeUuid):
    attribute_type = models.IntegerField(db_index=True)
    content_id = models.UUIDField(db_index=True)

class Attribute_DATE(dalmeBasic):
    attribute_id = models.ForeignKey('Attribute', to_field='id', db_index=True, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)
    value_day = models.IntegerField()
    value_month = models.IntegerField()
    value_year = models.IntegerField()

class Attribute_DBR(dalmeBasic):
    attribute_id = models.ForeignKey('Attribute', to_field='id', db_index=True, on_delete=models.CASCADE)
    value = models.CharField(max_length=32)

class Attribute_INT(dalmeBasic):
    attribute_id = models.ForeignKey('Attribute', to_field='id', db_index=True, on_delete=models.CASCADE)
    value = models.IntegerField()

class Attribute_STR(dalmeBasic):
    attribute_id = models.ForeignKey('Attribute', to_field='id', db_index=True, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

class Attribute_TXT(dalmeBasic):
    attribute_id = models.ForeignKey('Attribute', to_field='id', db_index=True, on_delete=models.CASCADE)
    value = models.TextField()

class Concept(dalmeUuid):
    getty_id = models.IntegerField(db_index=True)

class Content_class(dalmeIntid):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.TextField()

class Content_type(dalmeIntid):
    content_class = models.IntegerField()
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.TextField()

class Content_type_x_attribute_type(dalmeBasic):
    content_type = models.ForeignKey('Content_type', to_field='id', db_index=True, on_delete=models.CASCADE)
    attribute_type = models.ForeignKey('Attribute_type', to_field='id', db_index=True, on_delete=models.PROTECT)
    order = models.IntegerField(db_index=True)

class Headword(dalmeUuid):
    word = models.CharField(max_length=55)
    full_lemma = models.CharField(max_length=255)
    concept_id = models.ForeignKey('Concept', to_field='id', db_index=True, on_delete=models.PROTECT)

class Object(dalmeUuid):
    concept_id = models.UUIDField(db_index=True)
    object_phrase_id = models.ForeignKey('Object_phrase', to_field='id', db_index=True, on_delete=models.CASCADE)

class Object_attribute(dalmeBasic):
    object_id = models.ForeignKey('Object', to_field='id', db_index=True, on_delete=models.CASCADE)
    concept_id = models.UUIDField(db_index=True)

class Place(dalmeUuid):
    type = models.IntegerField(db_index=True)

class Source(dalmeUuid):
    type = models.IntegerField(db_index=True)
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    parent_source = models.UUIDField(null=True, default=None, db_index=True)
    is_inventory = models.BooleanField(default=False, db_index=True)

class Page(dalmeUuid):
    source_id = models.ForeignKey('Source', to_field='id', db_index=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=55)
    dam_id = models.IntegerField(db_index=True)
    order = models.IntegerField(db_index=True)

class Transcription(dalmeUuid):
    source_id = models.ForeignKey('Source', to_field='id', db_index=True, on_delete=models.CASCADE)
    transcription = models.TextField()

class Identity_phrase(dalmeUuid):
    transcription_id = models.ForeignKey('Transcription', to_field='id', db_index=True, on_delete=models.CASCADE)
    phrase = models.TextField()

class Object_phrase(dalmeUuid):
    transcription_id = models.ForeignKey('Transcription', to_field='id', db_index=True, on_delete=models.CASCADE)
    phrase = models.TextField()

class Word_form(dalmeUuid):
    normalized_form = models.CharField(max_length=55)
    pos = models.CharField(max_length=255)
    headword_id = models.ForeignKey('Headword', to_field='id', db_index=True, on_delete=models.PROTECT)

class Token(dalmeUuid):
    object_phrase_id = models.ForeignKey('Object_phrase', to_field='id', db_index=True, on_delete=models.CASCADE)
    word_form_id = models.ForeignKey('Word_form', to_field='id', db_index=True, on_delete=models.PROTECT)
    raw_token = models.CharField(max_length=255)
    clean_token = models.CharField(max_length=55)
    order = models.IntegerField(db_index=True)
    flags = models.CharField(max_length=10)

class Identity_phrase_x_entity(dalmeBasic):
    identity_phrase_id = models.ForeignKey('Identity_phrase', to_field='id', db_index=True, on_delete=models.CASCADE)
    entity_id = models.UUIDField(db_index=True)

#app management models
class error_message(dalmeBasic):
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
class par_inventory(dalmeUuid):
    title = models.CharField(max_length=255)
    source = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    series = models.CharField(max_length=16)
    shelf = models.CharField(max_length=32)
    transcriber = models.CharField(max_length=32)

class par_folio(dalmeUuid):
    inv_id = models.ForeignKey('par_inventory', on_delete=models.CASCADE)
    folio_no = models.CharField(max_length=32)
    dam_id = models.IntegerField()

class par_token(dalmeUuid):
    folio_id = models.ForeignKey('par_folio', on_delete=models.CASCADE)
    line_no = models.IntegerField()
    position = models.IntegerField()
    raw_token = models.CharField(max_length=64)
    clean_token = models.CharField(max_length=64)
    norm_token = models.CharField(max_length=64)
    token_type = models.CharField(max_length=32)
    flags = models.CharField(max_length=16, null=True, blank=True)
    span_start = models.IntegerField(null=True, blank=True)
    span_end = models.IntegerField(null=True, blank=True)

class par_object(models.Model):
    obj_id = models.IntegerField(primary_key=True, unique=True)
    ont_class = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    terms = models.CharField(max_length=255)
    material = models.CharField(max_length=64)
    room = models.CharField(max_length=64)
