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
from datetime import datetime

from dalme_app.modelTemplates import dalmeBasic, dalmeUuid, dalmeIntid
from dalme_app.scripts.db import wp_db, wiki_db, dam_db

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

class Attribute(dalmeUuid):
    attribute_type = models.ForeignKey(
        "Attribute_type",
        db_index=True,
        on_delete=models.PROTECT,
        db_column="attribute_type"
    )
    content_id = models.UUIDField(db_index=True)

    def get_data(self):
        for data_type in [
            'attribute_date',
            'attribute_dbr',
            'attribute_int',
            'attribute_str',
            'attribute_txt'
        ]:
            if hasattr(self,data_type):
                return eval('self.{}'.format(data_type))
        return None

class Attribute_DATE(dalmeBasic):
    attribute_id = models.OneToOneField(
        Attribute,
        db_index=True,
        on_delete=models.CASCADE
    )
    value = models.CharField(max_length=255)
    value_day = models.IntegerField()
    value_month = models.IntegerField()
    value_year = models.IntegerField()

class Attribute_DBR(dalmeBasic):
    attribute_id = models.OneToOneField(
        Attribute,
        db_index=True,
        on_delete=models.CASCADE
    )
    value = models.CharField(max_length=32)

class Attribute_INT(dalmeBasic):
    attribute_id = models.OneToOneField(
        Attribute,
        db_index=True,
        on_delete=models.CASCADE
    )
    value = models.IntegerField()

class Attribute_STR(dalmeBasic):
    attribute_id = models.OneToOneField(
        Attribute,
        db_index=True,
        on_delete=models.CASCADE
    )
    value = models.CharField(max_length=255)

class Attribute_TXT(dalmeBasic):
    attribute_id = models.ForeignKey(
        Attribute,
        db_index=True,
        on_delete=models.CASCADE
    )
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
    content_type = models.ForeignKey(
        'Content_type',
        to_field='id',
        db_index=True,
        on_delete=models.CASCADE
    )
    attribute_type = models.ForeignKey(
        'Attribute_type',
        to_field='id',
        db_index=True,
        on_delete=models.PROTECT
    )
    order = models.IntegerField(db_index=True)

class Headword(dalmeUuid):
    word = models.CharField(max_length=55)
    full_lemma = models.CharField(max_length=255)
    concept_id = models.ForeignKey(
        'Concept',
        to_field='id',
        db_index=True,
        on_delete=models.PROTECT
    )

class Object(dalmeUuid):
    concept_id = models.UUIDField(db_index=True)
    object_phrase_id = models.ForeignKey(
        'Object_phrase',
        to_field='id',
        db_index=True,
        on_delete=models.CASCADE
    )

class Object_attribute(dalmeBasic):
    object_id = models.ForeignKey(
        'Object',
        to_field='id',
        db_index=True,
        on_delete=models.CASCADE
    )
    concept_id = models.UUIDField(db_index=True)

class Place(dalmeUuid):
    type = models.IntegerField(db_index=True)

class Source(dalmeUuid):
    type = models.ForeignKey(
        'Content_type',
        to_field='id',
        db_index=True,
        on_delete=models.PROTECT,
        db_column="type"
    )
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    parent_source = models.ForeignKey(
        'self',
        on_delete=models.PROTECT,
        null=True,
        db_column="parent_source",

    )
    is_inventory = models.BooleanField(default=False, db_index=True)

    def get_fields(self):
        """
        Returns fields as a list of tuple pairs like (field_name, field_value)
        for use in templates
        """
        return [(field.name, field.value_to_string(self)) for field in Source._meta.fields]
    def get_attributes(self):
        """
        Returns associated attributes. This is a loose connection, with UUIDs
        in Attributes.content_id corresponding (potentially) to Sources
        """
        attributes = Attribute.objects.all().filter(content_id=self.pk)
        return attributes

class Page(dalmeUuid):
    source_id = models.ForeignKey(
        'Source',
        to_field='id',
        db_index=True,
        on_delete=models.CASCADE
    )
    name = models.CharField(max_length=55)
    dam_id = models.IntegerField(db_index=True)
    order = models.IntegerField(db_index=True)

class Transcription(dalmeUuid):
    source_id = models.ForeignKey(
        'Source',
        to_field='id',
        db_index=True,
        on_delete=models.CASCADE
    )
    transcription = models.TextField()

class Identity_phrase(dalmeUuid):
    transcription_id = models.ForeignKey(
        'Transcription',
        to_field='id',
        db_index=True,
        on_delete=models.CASCADE
    )
    phrase = models.TextField()

class Object_phrase(dalmeUuid):
    transcription_id = models.ForeignKey(
        'Transcription',
        to_field='id',
        db_index=True,
        on_delete=models.CASCADE
    )
    phrase = models.TextField()

class Word_form(dalmeUuid):
    normalized_form = models.CharField(max_length=55)
    pos = models.CharField(max_length=255)
    headword_id = models.ForeignKey(
        'Headword',
        to_field='id',
        db_index=True,
        on_delete=models.PROTECT
    )

class Token(dalmeUuid):
    object_phrase_id = models.ForeignKey(
        'Object_phrase',
        to_field='id',
        db_index=True,
        on_delete=models.CASCADE
    )
    word_form_id = models.ForeignKey(
        'Word_form',
        to_field='id',
        db_index=True,
        on_delete=models.PROTECT
    )
    raw_token = models.CharField(max_length=255)
    clean_token = models.CharField(max_length=55)
    order = models.IntegerField(db_index=True)
    flags = models.CharField(max_length=10)

class Identity_phrase_x_entity(dalmeBasic):
    identity_phrase_id = models.ForeignKey(
        'Identity_phrase',
        to_field='id',
        db_index=True,
        on_delete=models.CASCADE
    )
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
