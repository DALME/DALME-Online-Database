"""
This file defines all of the models used in the application. These models are
used to create database entries, and can be used in other functions to access
and iterate through data in the database without writing SQL statements.
"""
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.functional import cached_property
from dalme_app.middleware import get_current_user
import uuid, json, os, requests, logging, hashlib
from urllib.parse import urlencode
from datetime import datetime
from dalme_app.model_templates import dalmeBasic, dalmeUuid, dalmeIntid
import django.db.models.options as options
options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)

logger = logging.getLogger(__name__)

def rs_api_query(endpoint, user, key, **kwargs):
    sign = hashlib.sha256(key.encode('utf-8'))
    paramDict = kwargs
    paramDict['user'] = user
    paramstr = urlencode(paramDict)
    sign.update(paramstr.encode('utf-8'))
    R = requests.get(endpoint + paramstr + "&sign=" + sign.hexdigest())
    return R

class Profile(models.Model):
    """
    One-to-one extension of user model to accomodate additional user related
    data, including permissions of associated accounts on other platforms.
    """

    WP_ROLE = (
        ('a:1:{s:13:"administrator";b:1;}', 'Administrator'),
        ('a:1:{s:6:"editor";b:1;}', 'Editor'),
        ('a:1:{s:6:"author";b:1;}', 'Author'),
        ('a:1:{s:11:"contributor";b:1;}', 'Contributor'),
        ('a:1:{s:10:"subscriber";b:1;}', 'Subscriber')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=50, blank=True)
    dam_user = models.IntegerField(null=True)
    wiki_user = models.IntegerField(null=True)
    wp_user = models.IntegerField(null=True)
    wp_role = models.CharField(max_length=50, null=True, choices=WP_ROLE)

    def __str__(self):
        return self.user.username

    def get_dam_usergroup(self):
        dam_ug = rs_user.objects.get(ref=self.dam_user).usergroup
        return dam_ug

    def get_dam_usergroup_display(self):
        dam_ug = rs_user.objects.get(ref=self.dam_user).get_usergroup_display()
        return dam_ug

#DALME data store
class Agent(dalmeUuid):
    type = models.IntegerField()

class Attribute_type(dalmeIntid):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.TextField()
    data_type = models.CharField(max_length=15)
    source = models.CharField(max_length=255, null=True)
    same_as = models.CharField(max_length=55, null=True)

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
    attribute_type = models.ForeignKey('Attribute_type',to_field='id',db_index=True,on_delete=models.CASCADE)
    order = models.IntegerField(db_index=True)

class DT_list(dalmeIntid):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.TextField()
    default_headers = models.CharField(max_length=255, null=True)
    extra_headers = models.CharField(max_length=255, null=True)
    content_types = models.ManyToManyField(Content_type)
    api_url = models.CharField(max_length=255, null=True)
    form_helper = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']

class DT_fields(dalmeIntid):

    FILTER_OPS = (
        ('and', 'and'),
        ('or', 'or')
    )

    list = models.ForeignKey('DT_list', to_field='id', db_index=True, on_delete=models.CASCADE)
    field = models.ForeignKey('Attribute_type', to_field='id', db_index=True, on_delete=models.CASCADE)
    render_exp = models.CharField(max_length=255, null=True)
    orderable = models.BooleanField(default=False)
    visible = models.BooleanField(default=False)
    searchable = models.BooleanField(default=False)
    nowrap = models.BooleanField(default=False)
    dt_name = models.CharField(max_length=55, null=True)
    dte_name = models.CharField(max_length=55, null=True)
    dte_type = models.CharField(max_length=55, null=True)
    dte_options = models.CharField(max_length=255, null=True)
    dte_opts = models.CharField(max_length=255, null=True)
    is_filter = models.BooleanField(default=False)
    filter_type = models.CharField(max_length=55, null=True)
    filter_mode = models.CharField(max_length=55, null=True)
    filter_operator = models.CharField(max_length=55, null=True, choices=FILTER_OPS)
    filter_options = models.CharField(max_length=255, null=True)


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
    transcription_id = models.ForeignKey('Transcription', to_field='id', db_index=True, on_delete=models.SET_NULL, null=True, blank=True)

class Source(dalmeUuid):
    type = models.ForeignKey('Content_type', to_field='id', db_index=True, on_delete=models.PROTECT, db_column="type")
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    parent_source = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, db_column="parent_source")
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
    version = models.IntegerField(null=True)

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

class Notes(dalmeUuid):
    target = models.UUIDField(db_index=True)
    text = models.TextField()

#unmanaged models from DAM
class rs_resource(models.Model):
    ref = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200, null=True)
    resource_type = models.IntegerField(null=True)
    has_image = models.IntegerField(default='0')
    is_transcoding = models.IntegerField(default='0')
    hit_count = models.IntegerField(default='0')
    new_hit_count = models.IntegerField(default='0')
    creation_date = models.DateTimeField(null=True, blank=True)
    rating = models.IntegerField(null=True)
    user_rating = models.IntegerField(null=True)
    user_rating_count = models.IntegerField(null=True)
    user_rating_total = models.IntegerField(null=True)
    country = models.CharField(max_length=200, null=True)
    file_extension = models.CharField(max_length=10, null=True)
    preview_extension = models.CharField(max_length=10, null=True)
    image_red = models.IntegerField(null=True)
    image_green = models.IntegerField(null=True)
    image_blue = models.IntegerField(null=True)
    thumb_width = models.IntegerField(null=True)
    thumb_height = models.IntegerField(null=True)
    archive = models.IntegerField(default='0')
    access = models.IntegerField(default='0')
    colour_key = models.CharField(max_length=5, null=True)
    created_by = models.IntegerField(null=True)
    file_path = models.CharField(max_length=500, null=True)
    file_modified = models.DateTimeField(null=True, blank=True)
    file_checksum = models.CharField(max_length=32, null=True)
    request_count = models.IntegerField(default='0')
    expiry_notification_sent = models.IntegerField(default='0')
    preview_tweaks = models.CharField(max_length=50, null=True)
    geo_lat = models.FloatField(null=True)
    geo_long = models.FloatField(null=True)
    mapzoom = models.IntegerField(null=True)
    disk_usage = models.IntegerField(null=True)
    disk_usage_last_updated = models.DateTimeField(null=True, blank=True)
    file_size = models.IntegerField(null=True)
    preview_attempts = models.IntegerField(null=True)
    field12 = models.CharField(max_length=200, null=True)
    field8 = models.CharField(max_length=200, null=True)
    field3 = models.CharField(max_length=200, null=True)
    annotation_count = models.IntegerField(null=True)
    field51 = models.CharField(max_length=200, null=True)
    field79 = models.CharField(max_length=200, null=True)
    modified = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
       managed=False
       db_table='resource'
       in_db='dam'

class rs_resource_data(models.Model):
    resource = models.IntegerField(primary_key=True)
    resource_type_field = models.IntegerField(null=True)
    value = models.TextField()

    class Meta:
       managed=False
       db_table='resource_data'
       in_db='dam'

class rs_collection(models.Model):
    ref = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, null=True)
    user = models.IntegerField(null=True)
    created = models.DateTimeField(null=True, blank=True)
    public = models.IntegerField(default='0')
    theme = models.CharField(max_length=100, null=True)
    theme2 = models.CharField(max_length=100, null=True)
    theme3 = models.CharField(max_length=100, null=True)
    allow_changes = models.IntegerField(default='0')
    cant_delete = models.IntegerField(default='0')
    keywords = models.TextField()
    savedsearch = models.IntegerField(null=True)
    home_page_publish = models.IntegerField(null=True)
    home_page_text = models.TextField()
    home_page_image = models.IntegerField(null=True)
    session_id = models.IntegerField(null=True)
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
       managed=False
       db_table='collection'
       in_db='dam'

class rs_collection_resource(models.Model):
    collection = models.IntegerField(null=True)
    resource = models.IntegerField(null=True)
    date_added = models.DateTimeField(auto_now_add=True, primary_key=True)
    comment = models.TextField()
    rating = models.IntegerField(null=True)
    use_as_theme_thumbnail = models.IntegerField(null=True)
    purchase_size = models.CharField(max_length=10, null=True)
    purchase_complete = models.IntegerField(default='0')
    purchase_price = models.FloatField(max_length=10, default='0.00')
    sortorder = models.IntegerField(null=True)

    class Meta:
       managed=False
       db_table='collection_resource'
       in_db='dam'

class rs_user(models.Model):

    DAM_USERGROUPS = (
        (1, 'Administrator'),
        (2, 'General User'),
        (3, 'Super Admin'),
        (4, 'Archivist')
    )

    ref = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=64, null=True)
    fullname = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    usergroup = models.IntegerField(null=True, choices=DAM_USERGROUPS)
    last_active = models.DateTimeField(null=True, blank=True)
    logged_in = models.IntegerField(null=True)
    last_browser = models.TextField()
    last_ip = models.CharField(max_length=100, null=True)
    current_collection = models.IntegerField(null=True)
    accepted_terms = models.IntegerField(default='0')
    account_expires = models.DateTimeField(null=True, blank=True)
    comments = models.TextField()
    session = models.CharField(max_length=50, null=True)
    ip_restrict = models.TextField()
    search_filter_override = models.TextField()
    password_last_change = models.DateTimeField(null=True)
    login_tries = models.IntegerField(default='0')
    login_last_try = models.DateTimeField(null=True, blank=True)
    approved = models.IntegerField(default='1')
    lang = models.CharField(max_length=11, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    hidden_collections = models.TextField()
    password_reset_hash = models.CharField(max_length=100, null=True)
    origin = models.CharField(max_length=50, null=True)
    unique_hash = models.CharField(max_length=50, null=True)
    wp_authrequest = models.CharField(max_length=50, null=True)
    csrf_token = models.CharField(max_length=255, null=True)

    class Meta:
       managed=False
       db_table='user'
       in_db='dam'

class rs_resource_type_field(models.Model):
    ref = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50, null=True)
    title = models.CharField(max_length=400, null=True)
    type = models.IntegerField(null=True)
    order_by = models.IntegerField(default='0')
    keywords_index = models.IntegerField(default='0')
    partial_index = models.IntegerField(default='0')
    resource_type = models.IntegerField(default='0')
    resource_column = models.CharField(max_length=50, null=True)
    display_field = models.IntegerField(default='1')
    use_for_similar = models.IntegerField(default='1')
    iptc_equiv = models.CharField(max_length=20, null=True)
    display_template = models.TextField()
    tab_name = models.CharField(max_length=50, null=True)
    required = models.IntegerField(default='0')
    smart_theme_name = models.CharField(max_length=200, null=True)
    exiftool_field = models.CharField(max_length=200, null=True)
    advanced_search = models.IntegerField(default='1')
    simple_search = models.IntegerField(default='0')
    help_text = models.TextField()
    display_as_dropdown = models.IntegerField(default='0')
    external_user_access = models.IntegerField(default='1')
    autocomplete_macro = models.TextField()
    hide_when_uploading = models.IntegerField(default='0')
    hide_when_restricted = models.IntegerField(default='0')
    value_filter = models.TextField()
    exiftool_filter = models.TextField()
    omit_when_copying = models.IntegerField(default='0')
    tooltip_text = models.TextField()
    regexp_filter = models.CharField(max_length=400, null=True)
    sync_field = models.IntegerField(null=True)
    display_condition = models.CharField(max_length=400, null=True)
    onchange_macro = models.TextField()
    field_constraint = models.IntegerField(null=True)
    linked_data_field = models.TextField()
    automatic_nodes_ordering = models.IntegerField(default='0')
    fits_field = models.CharField(max_length=255, null=True)
    personal_data = models.IntegerField(default='0')

    class Meta:
       managed=False
       db_table='resource_type_field'
       in_db='dam'

#unmanaged models from WIKI
class wiki_user(models.Model):
    user_id = models.IntegerField(primary_key=True)
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
    user_editcount = models.IntegerField(null=True)
    user_password_expires = models.BinaryField(max_length=14, null=True)

    class Meta:
       managed=False
       db_table='user'
       in_db='wiki'

class wiki_user_groups(models.Model):

    WIKI_GROUPS = (
        ('users', 'Users'),
        ('administrator', 'Administrator'),
        ('bureaucrat', 'Bureaucrat'),
        ('sysop', 'Sysop')
    )

    ug_user = models.ForeignKey('wiki_user', to_field='user_id', db_index=True, on_delete=models.CASCADE, related_name='wiki_groups', db_column="ug_user")
    ug_group = models.BinaryField(max_length=255, choices=WIKI_GROUPS)
    ug_expiry = models.BinaryField(max_length=14, primary_key=True)

    class Meta:
       managed=False
       db_table='user_groups'
       in_db='wiki'

class wiki_page(models.Model):
    page_id = models.IntegerField(primary_key=True)
    page_namespace = models.IntegerField()
    page_title = models.BinaryField(max_length=255)
    page_restrictions = models.BinaryField()
    page_is_redirect = models.IntegerField(default='0')
    page_is_new = models.IntegerField(default='0')
    page_random = models.FloatField()
    page_touched = models.BinaryField(max_length=14)
    page_links_updated = models.BinaryField(max_length=14, null=True)
    page_latest = models.IntegerField()
    page_len = models.IntegerField()
    page_content_model = models.BinaryField(max_length=32, null=True)
    page_lang = models.BinaryField(max_length=35, null=True)

    class Meta:
       managed=False
       db_table='page'
       in_db='wiki'

#unmanaged models from WORDPRESS
class wp_users(models.Model):
    ID = models.IntegerField(primary_key=True)
    user_login = models.CharField(max_length=60, unique=True)
    user_pass = models.CharField(max_length=255)
    user_nicename = models.CharField(max_length=50)
    user_email = models.CharField(max_length=100)
    user_url = models.CharField(max_length=100)
    user_registered = models.DateTimeField(default='0000-00-00 00:00:00')
    user_activation_key = models.CharField(max_length=255)
    user_status = models.IntegerField(default='0')
    display_name = models.CharField(max_length=250)

    class Meta:
       managed=False
       db_table='wp_users'
       in_db='wp'


class wp_usermeta(models.Model):
    umeta_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(default='0')
    meta_key = models.CharField(max_length=255, null=True)
    meta_value = models.TextField()

    class Meta:
        managed=False
        db_table='wp_usermeta'
        in_db='wp'


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
