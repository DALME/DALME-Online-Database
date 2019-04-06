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
import uuid, json, os, requests, logging
from datetime import datetime
from dalme_app.modelTemplates import dalmeBasic, dalmeUuid, dalmeIntid
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)

logger = logging.getLogger(__name__)

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
        try:
            wp_user_exists = wp_users.objects.get(user_login=self.user.username).ID
            self.wp_userid = str(wp_user_exists)
        except:
            self.wp_userid = None

        # Set Wiki user ID, if it exists
        try:
            wiki_user_exists = wiki_user.objects.get(user_name=self.user.username).user_id
            self.wiki_userid = str(wiki_user_exists)
        except:
            self.wiki_userid = None

        # Set DAM user ID, if it exists
        try:
            dam_user_exists = rs_user.objects.get(username=self.user.username).ref
            self.dam_userid = str(dam_user_exists)
        except:
            self.dam_userid = None

    def create_accounts(self):
        """
        Create accounts in external platforms, so long as they don't have
        existing accounts
        """
        password = str(uuid.uuid4().hex)
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Wordpress user setup
        if self.wp_userid == None:
            new_wp_user = wp_users()
            new_wp_user.user_login = self.user.username
            new_wp_user.user_pass = password
            new_wp_user.user_nicename = self.user.username
            new_wp_user.user_email = self.user.email
            new_wp_user.user_registered = current_time
            new_wp_user.user_status = '0'
            new_wp_user.display_name = self.full_name
            new_wp_user.save()
            wp_userid = new_wp_user.ID
            self.wp_userid = wp_userid
            new_wp_meta = wp_usermeta()
            new_wp_meta.user_id = self.wp_userid
            new_wp_meta.meta_key = 'first_name'
            new_wp_meta.meta_value = self.user.first_name
            new_wp_meta.save()
            new_wp_meta = wp_usermeta()
            new_wp_meta.user_id = self.wp_userid
            new_wp_meta.meta_key = 'last_name'
            new_wp_meta.meta_value = self.user.last_name
            new_wp_meta.save()

        # Wiki user setup
        if self.wiki_userid == None:
            new_wiki_user = wiki_users()
            new_wiki_user.user_name = self.user.username
            new_wiki_user.user_real_name = self.full_name
            new_wiki_user.user_password = password
            new_wiki_user.user_newpassword = password
            new_wiki_user.user_email = self.user.email
            new_wiki_user.save()
            wiki_userid = new_wiki_user.user_id
            self.wiki_userid = wiki_userid

        if self.dam_userid == None:
            if self.dam_usergroup:
                usergroup = self.dam_usergroup
            else:
                usergroup = 2
            new_dam_user = rs_user()
            new_dam_user.username = self.user.username
            new_dam_user.password = password
            new_dam_user.fullname = self.full_name
            new_dam_user.email = self.user.email
            new_dam_user.usergroup = usergroup
            new_dam_user.approved = 1
            new_dam_user.save()
            dam_userid = new_dam_user.ref
            self.dam_userid = dam_userid

    def push_permissions(self):
        """
        Updates external accounts with permissions set in user management here
        """
        if self.wp_userid != None and self.wp_role != None:
            new_wp_meta = wp_usermeta()
            new_wp_meta.user_id = self.wp_userid
            new_wp_meta.meta_key = 'wp_capabilities'
            new_wp_meta.meta_value = self.wp_role
            new_wp_meta.save()

        if self.wiki_userid != None and self.wiki_groups != None:
            wiki_group_dict = {
                "administrator":"sysop",
                "bureaucrat":"bureaucrat"
            }
            for group in self.wiki_groups:
                if group in wiki_group_dict:
                    wiki_ug = wiki_user_groups()
                    wiki_ug.ug_user = self.wiki_userid
                    wiki_ug.ug_group = wiki_group_dict[group]
                    wiki_ug.save()

        if self.dam_userid != None and self.dam_usergroup != None:
            dam_user = rs_user.objects.get(ref=self.dam_userid)
            dam_user.usergroup = self.dam_usergroup
            dam_user.save()


    def delete_external_accounts(self):
        """
        Deletes all external accounts associated with this account
        """
        # Delete Wordpress account
        wp_user = wp_users.objects.get(user_login=self.user.username)
        wp_user.delete()
        # Delete wiki account
        wiki_user = wiki_user.objects.get(user_name=self.user.username)
        wiki_user.delete()
        # Delete DAM account
        dam_user = rs_user.objects.get(username=self.user.username)
        dam_user.delete()

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
    dam_id = models.IntegerField(db_index=True, null=True, blank=True)
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

#unmanaged models from DAM
class rs_resource(models.Model):
    ref = models.IntegerField(primary_key=True, max_length=11)
    title = models.CharField(max_length=200, null=True)
    resource_type = models.IntegerField(max_length=11, null=True)
    has_image = models.IntegerField(max_length=11, default='0')
    is_transcoding = models.IntegerField(max_length=11, default='0')
    hit_count = models.IntegerField(max_length=11, default='0')
    new_hit_count = models.IntegerField(max_length=11, default='0')
    creation_date = models.DateTimeField(null=True, blank=True)
    rating = models.IntegerField(max_length=11, null=True)
    user_rating = models.IntegerField(max_length=11, null=True)
    user_rating_count = models.IntegerField(max_length=11, null=True)
    user_rating_total = models.IntegerField(max_length=11, null=True)
    country = models.CharField(max_length=200, null=True)
    file_extension = models.CharField(max_length=10, null=True)
    preview_extension = models.CharField(max_length=10, null=True)
    image_red = models.IntegerField(max_length=11, null=True)
    image_green = models.IntegerField(max_length=11, null=True)
    image_blue = models.IntegerField(max_length=11, null=True)
    thumb_width = models.IntegerField(max_length=11, null=True)
    thumb_height = models.IntegerField(max_length=11, null=True)
    archive = models.IntegerField(max_length=11, default='0')
    access = models.IntegerField(max_length=11, default='0')
    colour_key = models.CharField(max_length=5, null=True)
    created_by = models.IntegerField(max_length=11, null=True)
    file_path = models.CharField(max_length=500, null=True)
    file_modified = models.DateTimeField(null=True, blank=True)
    file_checksum = models.CharField(max_length=32, null=True)
    request_count = models.IntegerField(max_length=11, default='0')
    expiry_notification_sent = models.IntegerField(max_length=11, default='0')
    preview_tweaks = models.CharField(max_length=50, null=True)
    geo_lat = models.FloatField(null=True)
    geo_long = models.FloatField(null=True)
    mapzoom = models.IntegerField(max_length=11, null=True)
    disk_usage = models.IntegerField(max_length=20, null=True)
    disk_usage_last_updated = models.DateTimeField(null=True, blank=True)
    file_size = models.IntegerField(max_length=20, null=True)
    preview_attempts = models.IntegerField(max_length=11, null=True)
    field12 = models.CharField(max_length=200, null=True)
    field8 = models.CharField(max_length=200, null=True)
    field3 = models.CharField(max_length=200, null=True)
    annotation_count = models.IntegerField(max_length=11, null=True)
    field51 = models.CharField(max_length=200, null=True)
    field79 = models.CharField(max_length=200, null=True)
    modified = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
       managed = False
       db_table = 'resource'
       in_db = 'dam'

class rs_resource_data(models.Model):
    resource = models.IntegerField(max_length=11, null=True, primary_key=True)
    resource_type_field = models.IntegerField(max_length=11, null=True)
    value = models.TextField()

    class Meta:
       managed = False
       db_table = 'resource_data'
       in_db = 'dam'

class rs_collection(models.Model):
    ref = models.IntegerField(primary_key=True, max_length=11)
    name = models.CharField(max_length=100, null=True)
    user = models.IntegerField(max_length=11, null=True)
    created = models.DateTimeField(null=True, blank=True)
    public = models.IntegerField(max_length=11, default='0')
    theme = models.CharField(max_length=100, null=True)
    theme2 = models.CharField(max_length=100, null=True)
    theme3 = models.CharField(max_length=100, null=True)
    allow_changes = models.IntegerField(max_length=11, default='0')
    cant_delete = models.IntegerField(max_length=11, default='0')
    keywords = models.TextField()
    savedsearch = models.IntegerField(max_length=11, null=True)
    home_page_publish = models.IntegerField(max_length=11, null=True)
    home_page_text = models.TextField()
    home_page_image = models.IntegerField(max_length=11, null=True)
    session_id = models.IntegerField(max_length=11, null=True)
    theme4 = models.CharField(max_length=100, null=True)
    theme5 = models.CharField(max_length=100, null=True)
    theme6 = models.CharField(max_length=100, null=True)
    theme7 = models.CharField(max_length=100, null=True)
    theme8 = models.CharField(max_length=100, null=True)
    theme9 = models.CharField(max_length=100, null=True)
    theme10 = models.CharField(max_length=100, null=True)
    theme11 = models.CharField(max_length=100, null=True)
    theme12 = models.CharField(max_length=100, null=True)
    theme13 = models.CharField(max_length=100, null=True)
    theme14 = models.CharField(max_length=100, null=True)
    theme15 = models.CharField(max_length=100, null=True)
    theme16 = models.CharField(max_length=100, null=True)
    theme17 = models.CharField(max_length=100, null=True)
    theme18 = models.CharField(max_length=100, null=True)
    theme19 = models.CharField(max_length=100, null=True)
    theme20 = models.CharField(max_length=100, null=True)

    class Meta:
       managed = False
       db_table = 'collection'
       in_db = 'dam'

class rs_collection_resource(models.Model):
    collection = models.IntegerField(max_length=11, null=True)
    resource = models.IntegerField(max_length=11, null=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True, blank=True, primary_key=True)
    comment = models.TextField()
    rating = models.IntegerField(max_length=11, null=True)
    use_as_theme_thumbnail = models.IntegerField(max_length=11, null=True)
    purchase_size = models.CharField(max_length=10, null=True)
    purchase_complete = models.IntegerField(max_length=11, default='0')
    purchase_price = models.FloatField(max_length=10, default='0.00')
    sortorder = models.IntegerField(max_length=11, null=True)

    class Meta:
       managed = False
       db_table = 'collection_resource'
       in_db = 'dam'

class rs_user(models.Model):
    ref = models.IntegerField(primary_key=True, max_length=11)
    username = models.CharField(max_length=50, null=True)
    password = models.CharField(max_length=64, null=True)
    fullname = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    usergroup = models.IntegerField(max_length=11, null=True)
    last_active = models.DateTimeField(null=True, blank=True)
    logged_in = models.IntegerField(max_length=11, null=True)
    last_browser = models.TextField()
    last_ip = models.CharField(max_length=100, null=True)
    current_collection = models.IntegerField(max_length=11, null=True)
    accepted_terms = models.IntegerField(max_length=11, default='0')
    account_expires = models.DateTimeField(null=True, blank=True)
    comments = models.TextField()
    session = models.CharField(max_length=50, null=True)
    ip_restrict = models.TextField()
    search_filter_override = models.TextField()
    password_last_change = models.DateTimeField(null=True)
    login_tries = models.IntegerField(max_length=11, default='0')
    login_last_try = models.DateTimeField(null=True, blank=True)
    approved = models.IntegerField(max_length=11, default='1')
    lang = models.CharField(max_length=11, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    hidden_collections = models.TextField()
    password_reset_hash = models.CharField(max_length=100, null=True)
    origin = models.CharField(max_length=50, null=True)
    unique_hash = models.CharField(max_length=50, null=True)
    wp_authrequest = models.CharField(max_length=50, null=True)
    csrf_token = models.CharField(max_length=255, null=True)

    class Meta:
       managed = False
       db_table = 'user'
       in_db = 'dam'

class rs_resource_type_field(models.Model):
    ref = models.IntegerField(primary_key=True, max_length=11)
    name = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=400, null=True)
    type = models.IntegerField(max_length=11, null=True)
    order_by = models.IntegerField(max_length=11, default='0')
    keywords_index = models.IntegerField(max_length=11, default='0')
    partial_index = models.IntegerField(max_length=11, default='0')
    resource_type = models.IntegerField(max_length=11, default='0')
    resource_column = models.CharField(max_length=50, null=True)
    display_field = models.IntegerField(max_length=11, default='1')
    use_for_similar = models.IntegerField(max_length=11, default='1')
    iptc_equiv = models.CharField(max_length=20, null=True)
    display_template = models.TextField()
    tab_name = models.CharField(max_length=50, null=True)
    required = models.IntegerField(max_length=11, default='0')
    smart_theme_name = models.CharField(max_length=200, null=True)
    exiftool_field = models.CharField(max_length=200, null=True)
    advanced_search = models.IntegerField(max_length=11, default='1')
    simple_search = models.IntegerField(max_length=11, default='0')
    help_text = models.TextField()
    display_as_dropdown = models.IntegerField(max_length=11, default='0')
    external_user_access = models.IntegerField(max_length=11, default='1')
    autocomplete_macro = models.TextField()
    hide_when_uploading = models.IntegerField(max_length=11, default='0')
    hide_when_restricted = models.IntegerField(max_length=11, default='0')
    value_filter = models.TextField()
    exiftool_filter = models.TextField()
    omit_when_copying = models.IntegerField(max_length=11, default='0')
    tooltip_text = models.TextField()
    regexp_filter = models.CharField(max_length=400, null=True)
    sync_field = models.IntegerField(max_length=11, null=True)
    display_condition = models.CharField(max_length=400, null=True)
    onchange_macro = models.TextField()
    field_constraint = models.IntegerField(max_length=11, null=True)
    linked_data_field = models.TextField()
    automatic_nodes_ordering = models.IntegerField(max_length=1, default='0')
    fits_field = models.CharField(max_length=255, null=True)
    personal_data = models.IntegerField(max_length=1, default='0')

    class Meta:
       managed = False
       db_table = 'resource_type_field'
       in_db = 'dam'

#unmanaged models from WIKI
class wiki_user(models.Model):
    user_id = models.IntegerField(primary_key=True, max_length=10)
    user_name = models.BinaryField(max_length=255, unique=True)
    user_real_name = models.BinaryField(max_length=255)
    user_password = models.BinaryField()
    user_newpassword = models.BinaryField()
    user_newpass_time = models.BinaryField(max_length=14, null=True)
    user_email = models.BinaryField()
    user_touched = models.BinaryField(max_length=14)
    user_token = models.BinaryField(max_length=32)
    user_email_authenticated = models.BinaryField(max_length=14, null=True)
    user_email_token = models.BinaryField(max_length=32, null=True)
    user_email_token_expires = models.BinaryField(max_length=14, null=True)
    user_registration = models.BinaryField(max_length=14, null=True)
    user_editcount = models.IntegerField(max_length=11, null=True)
    user_password_expires = models.BinaryField(max_length=14, null=True)

    class Meta:
       managed = False
       db_table = 'user'
       in_db = 'wiki'

class wiki_user_groups(models.Model):
    ug_user = models.IntegerField(max_length=10, default='0')
    ug_group = models.BinaryField(max_length=255)
    ug_expiry = models.BinaryField(max_length=14, null=True)

    class Meta:
       managed = False
       db_table = 'user_groups'
       in_db = 'wiki'

class wiki_page(models.Model):
    page_id = models.IntegerField(primary_key=True, max_length=10)
    page_namespace = models.IntegerField(max_length=11)
    page_title = models.BinaryField(max_length=255)
    page_restrictions = models.BinaryField()
    page_is_redirect = models.IntegerField(max_length=3, default='0')
    page_is_new = models.IntegerField(max_length=3, default='0')
    page_random = models.FloatField()
    page_touched = models.BinaryField(max_length=14)
    page_links_updated = models.BinaryField(max_length=14, null=True)
    page_latest = models.IntegerField(max_length=10)
    page_len = models.IntegerField(max_length=10)
    page_content_model = models.BinaryField(max_length=32, null=True)
    page_lang = models.BinaryField(max_length=35, null=True)

    class Meta:
       managed = False
       db_table = 'page'
       in_db = 'wiki'

#unmanaged models from WORDPRESS
class wp_users(models.Model):
    ID = models.IntegerField(primary_key=True, max_length=20)
    user_login = models.CharField(max_length=60)
    user_pass = models.CharField(max_length=255)
    user_nicename = models.CharField(max_length=50)
    user_email = models.CharField(max_length=100)
    user_url = models.CharField(max_length=100)
    user_registered = models.DateTimeField(default='0000-00-00 00:00:00')
    user_activation_key = models.CharField(max_length=255)
    user_status = models.IntegerField(max_length=11, default='0')
    display_name = models.CharField(max_length=250)

    class Meta:
       managed = False
       db_table = 'wp_users'
       in_db = 'wp'


class wp_usermeta(models.Model):
    umeta_id = models.IntegerField(primary_key=True, max_length=20)
    user_id = models.IntegerField(max_length=20, default='0')
    meta_key = models.CharField(max_length=255, null=True)
    meta_value = models.TextField()

    class Meta:
        managed = False
        db_table = 'wp_usermeta'
        in_db = 'wp'


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
