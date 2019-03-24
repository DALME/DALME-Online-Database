"""
This file defines all of the models used in the application. These models are
used to create database entries, and can be used in other functions to access
and iterate through data in the database without writing SQL statements.
"""

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.functional import cached_property
from dalme_app.middleware import get_current_user

import uuid
import json
import os
from datetime import datetime
import requests
import logging
logger = logging.getLogger(__name__)

from dalme_app.modelTemplates import dalmeBasic, dalmeUuid, dalmeIntid

try:
    from dalme_app.scripts.db import wp_db, wiki_db, dam_db
    from dalme_app.scripts.dam import rs_api_query
except:
    logger.debug("Can't connect to MySQL instance containing Wiki, DAM, and WP databases.")



#function for creating UUIDs - not used, but migrations won't work without it
def make_uuid():
    the_id = uuid.uuid4().hex
    return the_id


class Profile(models.Model):
    """
    One-to-one extension of user model to accomodate additional user related
    data, including permissions of associated accounts on other platforms.
    """
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

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=50, blank=True)
    dam_userid = models.IntegerField(null=True)
    dam_usergroup = models.IntegerField(choices=DAM_USERGROUPS, null=True)
    wiki_userid = models.IntegerField(null=True)
    wiki_username = models.CharField(max_length=50, null=True)
    wiki_groups = models.CharField(max_length=255, null=True)
    wp_userid = models.IntegerField(null=True)
    wp_role = models.CharField(max_length=50, null=True, choices=WP_ROLE)
    wp_avatar_url = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.user.username

    def pull_ids(self):
        """
        For a given user, set external identifiers for associated accounts.
        These accounts have the same username as the associated user object
        """
        # Set Wordpress user ID, if it exists
        wp_cursor = wp_db.cursor()
        wp_user_exists = wp_cursor.execute("SELECT ID FROM wp_users WHERE user_login = %s",[self.user.username])
        print(wp_user_exists)
        if wp_user_exists:
            self.wp_userid = wp_cursor.fetchone()[0]
        else:
            self.wp_userid = None
        wp_cursor.close()
        # Set Wiki user ID, if it exists
        wiki_cursor = wiki_db.cursor()
        wiki_user_exists = wiki_cursor.execute("SELECT user_id FROM user WHERE user_name = %s",[self.user.username])
        if wiki_user_exists:
            self.wiki_userid = wiki_cursor.fetchone()[0]
        else:
            self.wiki_userid = None
        wiki_cursor.close()
        # Set DAM user ID, if it exists
        wiki_cursor = dam_db.cursor()
        wiki_user_exists = wiki_cursor.execute("SELECT ref FROM user WHERE username = %s",[self.user.username])
        if wiki_user_exists:
            self.dam_userid = wiki_cursor.fetchone()[0]
        else:
            self.dam_userid = None
        wiki_cursor.close()

    def create_accounts(self):
        """
        Create accounts in external platforms, so long as they don't have
        existing accounts
        """
        password = str(uuid.uuid4().hex)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Wordpress user setup
        if self.wp_userid == None:
            wp_cursor = wp_db.cursor()
            wp_cursor.execute(
                ("INSERT INTO wp_users ("
                    "user_login,"
                    "user_pass,"
                    "user_nicename,"
                    "user_email,"
                    "user_registered,"
                    "user_status,"
                    "display_name"
                ") VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s')") % (
                    self.user.username,
                    password,
                    self.user.username,
                    self.user.email,
                    current_time,
                    '0',
                    self.full_name
                ))
            wp_cursor.execute("SELECT ID FROM wp_users WHERE user_login = %s", [self.user.username])
            wp_userid = wp_cursor.fetchone()[0]
            self.wp_userid = wp_userid
            wp_cursor.execute(
                ("INSERT INTO wp_usermeta ("
                    "user_id,"
                    "meta_key,"
                    "meta_value"
                ") VALUES ('%s', %s, %s)"), (
                    self.wp_userid,
                    'first_name',
                    self.user.first_name
                )
            )
            wp_cursor.execute(
                ("INSERT INTO wp_usermeta ("
                    "user_id,"
                    "meta_key,"
                    "meta_value"
                ") VALUES ('%s', %s, %s)"), (
                    self.wp_userid,
                    'last_name',
                    self.user.last_name
                )
            )
            wp_db.commit()
            wp_cursor.close()
        # Wiki user setup
        if self.wiki_userid == None:
            wiki_cursor = wiki_db.cursor()
            wiki_cursor.execute(
                ('INSERT INTO user ('
                    'user_name,'
                    'user_real_name,'
                    'user_password,'
                    'user_newpassword,'
                    'user_email'
                ') VALUES ("%s", "%s", "%s", "%s", "%s")' % (
                    self.user.username,
                    self.full_name,
                    password,
                    password,
                    self.user.email
                ))
            )
            wiki_cursor.execute('SELECT user_id FROM user WHERE user_name = %s',[self.user.username])
            wiki_userid = wiki_cursor.fetchone()[0]
            self.wiki_userid = wiki_userid
            wiki_db.commit()
            wiki_cursor.close()
        if self.dam_userid == None:
            dam_cursor = dam_db.cursor()
            if self.dam_usergroup:
                usergroup = self.dam_usergroup
            else:
                usergroup = 2
            dam_cursor.execute(
                ('INSERT INTO user ('
                    'username,'
                    'password,'
                    'fullname,'
                    'email,'
                    'usergroup,'
                    'approved'
                ') VALUES ("%s", "%s", "%s", "%s", "%s", "%s")' % (
                    self.user.username,
                    password,
                    self.full_name,
                    self.user.email,
                    usergroup,
                    1
                ))
            )
            dam_cursor.execute('SELECT ref FROM user WHERE username = %s',[self.user.username])
            dam_userid = dam_cursor.fetchone()[0]
            self.dam_userid = dam_userid
            wiki_db.commit()
            dam_cursor.close()

    def push_permissions(self):
        """
        Updates external accounts with permissions set in user management here
        """
        if self.wp_userid != None and self.wp_role != None:
            wp_cursor = wp_db.cursor()
            wp_cursor.execute(
                ("INSERT INTO wp_usermeta ("
                    "user_id,"
                    "meta_key,"
                    "meta_value"
                ") VALUES({}, {}, {})").format(
                    wp_userid,
                    'wp_capabilities',
                    wp_role
                )
            )
            wp_db.commit()
            wp_cursor.close()
        if self.wiki_userid != None and self.wiki_groups != None:
            wiki_cursor = wiki_db.cursor()
            wiki_group_dict = {
                "administrator":"sysop",
                "bureaucrat":"bureaucrat"
            }
            for group in self.wiki_groups:
                if group in wiki_group_dict:
                    wiki_cursor.execute(
                        ("INSERT INTO user_groups ("
                            "ug_user,"
                            "ug_group"
                        ") VALUES ({}, {})").format(
                            wiki_userid,
                            wiki_group_dict[group]
                        )
                    )
            wiki_db.commit()
            wiki_cursor.close()
        if self.dam_userid != None and self.dam_usergroup != None:
            dam_cursor = dam_db.cursor()
            dam_cursor.execute(
                ("UPDATE users"
                 "SET (usergroup) "
                 "VALUES ({}) WHERE ref={}").format(
                    self.dam_usergroup,
                    self.dam_userid
                )
            )
            dam_db.commit()
            dam_cursor.close()


    def delete_external_accounts(self):
        """
        Deletes all external accounts associated with this account
        """
        # Delete Wordpress account
        wp_cursor=wp_db.cursor()
        wp_cursor.execute('DELETE FROM wp_users WHERE user_login=%s',[self.user.username])
        wp_db.commit()
        wp_cursor.close()
        # Delete wiki account
        wiki_cursor=wiki_db.cursor()
        wiki_cursor.execute('DELETE FROM user WHERE user_name=%s',[self.user.username])
        wiki_db.commit()
        wiki_cursor.close()
        # Delete DAM account
        dam_cursor=dam_db.cursor()
        dam_cursor.execute('DELETE FROM user WHERE username=%s',[self.user.username])
        dam_db.commit()
        dam_cursor.close()

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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']

class Attribute(dalmeUuid):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.UUIDField(null=True, db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    attribute_type = models.ForeignKey("Attribute_type", db_index=True, on_delete=models.PROTECT, db_column="attribute_type")
    value_STR = models.CharField(max_length=255, blank=True, null=True)
    value_DATE_d = models.IntegerField(blank=True, null=True)
    value_DATE_m = models.IntegerField(blank=True, null=True)
    value_DATE_y = models.IntegerField(blank=True, null=True)
    value_DATE = models.DateField(blank=True, null=True)
    value_DBR = models.UUIDField(blank=True, null=True)
    value_INT = models.IntegerField(blank=True, null=True)
    value_TXT = models.TextField(blank=True, null=True)

    #need function that generates DATE field + string value on save

    def __str__(self):
        if self.data_type == 'DATE':
            str_val = self.value_STR
        else:
            str_val = eval('self.value_' + self.data_type)
            str_val = str(str_val)
        return str_val

class Concept(dalmeUuid):
    getty_id = models.IntegerField(db_index=True)

class Content_class(dalmeIntid):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']

class Content_type(dalmeIntid):
    content_class = models.IntegerField()
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.TextField()
    attribute_types = models.ManyToManyField(Attribute_type, through='Content_attributes')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']

class Content_attributes(dalmeIntid):
    content_type = models.ForeignKey('Content_type',to_field='id',db_index=True,on_delete=models.CASCADE)
    attribute_type = models.ForeignKey('Attribute_type',to_field='id',db_index=True,on_delete=models.PROTECT)
    order = models.IntegerField(db_index=True)

class Content_list(dalmeIntid):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.TextField()
    default_headers = models.CharField(max_length=255, null=True)
    extra_headers = models.CharField(max_length=255, null=True)
    content_types = models.ManyToManyField(Content_type)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']

class Headword(dalmeUuid):
    word = models.CharField(max_length=55)
    full_lemma = models.CharField(max_length=255)
    concept_id = models.ForeignKey('Concept', to_field='id', db_index=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.word

class Object(dalmeUuid):
    concept_id = models.UUIDField(db_index=True)
    object_phrase_id = models.ForeignKey('Object_phrase', to_field='id', db_index=True, on_delete=models.CASCADE)

class Object_attribute(dalmeBasic):
    object_id = models.ForeignKey('Object', to_field='id', db_index=True, on_delete=models.CASCADE)
    concept_id = models.UUIDField(db_index=True)

class Place(dalmeUuid):
    type = models.IntegerField(db_index=True)

class Page(dalmeUuid):
    name = models.CharField(max_length=55)
    dam_id = models.IntegerField(db_index=True)
    order = models.IntegerField(db_index=True)
    canvas = models.TextField(null=True)

    def __str__(self):
        return self.name
    def get_absolute_url(self):
        return reverse('page_detail', kwargs={'pk':self.pk})
    def get_canvas(self):
        if not self.canvas:
            api_params = {
                "function": "get_resource_data",
                "param1": self.dam_id
            }
            page_meta = rs_api_query(
                "https://dam.dalme.org/api/?",
                os.environ['DAM_API_USER'],
                os.environ['DAM_API_KEY'],
                **api_params
            )
            page_meta_obj = page_meta.json()
            if type(page_meta_obj) == list:
                folio = page_meta_obj[0]['field79']
            elif type(page_meta_obj) == dict:
                folio = page_meta_obj['field79']
            canvas = requests.get(
                "https://dam.dalme.org/iiif/{}/canvas/{}".format(self.dam_id,folio)
            )
            self.canvas = canvas.text
            return canvas.text
        else:
            return self.canvas

class Source_pages(dalmeIntid):
    source_id = models.ForeignKey('Source', to_field='id', db_index=True, on_delete=models.CASCADE)
    page_id = models.ForeignKey('Page', to_field='id', db_index=True, on_delete=models.CASCADE)
    transcription_id = models.ForeignKey('Transcription', to_field='id', db_index=True, on_delete=models.PROTECT, null=True, blank=True)

class Source(dalmeUuid):
    type = models.ForeignKey('Content_type', to_field='id', db_index=True, on_delete=models.PROTECT, db_column="type")
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    parent_source = models.ForeignKey('self', on_delete=models.PROTECT, null=True, db_column="parent_source")
    is_inventory = models.BooleanField(default=False, db_index=True)
    attributes = GenericRelation(Attribute, related_query_name='sources')
    pages = models.ManyToManyField(Page, db_index=True, through='Source_pages')

    def __str__(self):
        return self.short_name

    def get_absolute_url(self):
        return reverse('source_detail', kwargs={'pk':self.pk})

class Transcription(dalmeUuid):
    transcription = models.TextField(blank=True, null=True)
    author = models.CharField(max_length=255, default=get_current_user)

    def __str__(self):
        return str(self.id)

class Identity_phrase(dalmeUuid):
    transcription_id = models.ForeignKey('Transcription', to_field='id', db_index=True, on_delete=models.CASCADE)
    phrase = models.TextField()

    def __str__(self):
        return self.phrase

class Object_phrase(dalmeUuid):
    transcription_id = models.ForeignKey('Transcription', to_field='id', db_index=True, on_delete=models.CASCADE)
    phrase = models.TextField()

    def __str__(self):
        return self.phrase

class Wordform(dalmeUuid):
    normalized_form = models.CharField(max_length=55)
    pos = models.CharField(max_length=255)
    headword_id = models.ForeignKey('Headword', to_field='id', db_index=True, on_delete=models.PROTECT)

    def __str__(self):
        return self.normalized_form

class Token(dalmeUuid):
    object_phrase_id = models.ForeignKey('Object_phrase', to_field='id', db_index=True, on_delete=models.CASCADE)
    wordform_id = models.ForeignKey('Wordform', to_field='id', db_index=True, on_delete=models.PROTECT)
    raw_token = models.CharField(max_length=255)
    clean_token = models.CharField(max_length=55)
    order = models.IntegerField(db_index=True)
    flags = models.CharField(max_length=10)

    def __str__(self):
        return self.raw_token

class Identity_phrase_x_entity(dalmeBasic):
    identity_phrase_id = models.ForeignKey('Identity_phrase', to_field='id', db_index=True, on_delete=models.CASCADE)
    entity_id = models.UUIDField(db_index=True)

#app management models
class Notification(dalmeIntid):
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
    code = models.IntegerField(unique=True, db_index=True)
    level = models.IntegerField(choices=LEVELS)
    type = models.IntegerField(choices=TYPES)
    text = models.TextField()

class AttributeReference(dalmeUuid):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.TextField()
    data_type = models.CharField(max_length=15)
    source = models.CharField(max_length=255)
    term_type = models.CharField(max_length=55, blank=True, null=True)

class Comment(dalmeUuid):
    target = models.UUIDField(db_index=True)
    text = models.TextField()

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
