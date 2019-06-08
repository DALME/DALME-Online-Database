"""
This file defines all of the models used in the application. These models are
used to create database entries, and can be used in other functions to access
and iterate through data in the database without writing SQL statements.
"""
from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from dalme_app.middleware import get_current_user, get_current_username
import os
import json
import requests
import hashlib
import textwrap
from urllib.parse import urlencode
import datetime
from dalme_app.model_templates import dalmeBasic, dalmeUuid, dalmeIntid
import django.db.models.options as options
from django.utils.dateparse import parse_date
import calendar
import mimetypes
from django.conf import settings

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


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
        ('a:1:{s:10:"subscriber";b:1;}', 'Subscriber'),
        ('a:1:{s:11:"contributor";b:1;}', 'Contributor'),
        ('a:1:{s:6:"author";b:1;}', 'Author'),
        ('a:1:{s:6:"editor";b:1;}', 'Editor'),
        ('a:1:{s:13:"administrator";b:1;}', 'Administrator'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    full_name = models.CharField(max_length=50, blank=True)
    dam_user = models.IntegerField(null=True)
    wiki_user = models.IntegerField(null=True)
    wp_user = models.IntegerField(null=True)
    wp_role = models.CharField(max_length=50, blank=True, choices=WP_ROLE, default='a:1:{s:10:"subscriber";b:1;}')
    profile_image = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.username

    def get_dam_usergroup(self):
        dam_ug = rs_user.objects.get(ref=self.dam_user).usergroup
        return dam_ug

    def get_dam_usergroup_display(self):
        dam_ug = rs_user.objects.get(ref=self.dam_user).get_usergroup_display()
        return dam_ug

# DALME data store


class Agent(dalmeUuid):
    type = models.IntegerField()
    tags = GenericRelation('Tag')


class Attribute_type(dalmeIntid):

    DATA_TYPES = (
        ('DATE', 'DATE (date)'),
        ('INT', 'INT (integer)'),
        ('STR', 'STR (string)'),
        ('TXT', 'TXT (text)')
    )

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55, unique=True)
    description = models.TextField()
    data_type = models.CharField(max_length=15, choices=DATA_TYPES)
    source = models.CharField(max_length=255, blank=True, null=True, default=None)
    same_as = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, db_column="same_as")
    options_list = models.CharField(max_length=255, blank=True, null=True, default=None)

    def __str__(self):
        return self.name + ' ('+self.short_name+')'

    class Meta:
        ordering = ['id']


class Attribute(dalmeUuid):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.UUIDField(null=True, db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    attribute_type = models.ForeignKey("Attribute_type", db_index=True, on_delete=models.CASCADE, db_column="attribute_type")
    value_STR = models.CharField(max_length=255, blank=True, null=True, default=None)
    value_DATE_d = models.IntegerField(blank=True, null=True)
    value_DATE_m = models.IntegerField(blank=True, null=True)
    value_DATE_y = models.IntegerField(blank=True, null=True)
    value_DATE = models.DateField(blank=True, null=True)
    value_INT = models.IntegerField(blank=True, null=True)
    value_TXT = models.TextField(blank=True, default=None)

    def __str__(self):
        if self.attribute_type.data_type == 'DATE':
            str_val = self.value_STR
        else:
            str_val = str(eval('self.value_' + self.attribute_type.data_type))
        return str_val

    def save(self, *args, **kwargs):
        if self.attribute_type.data_type == 'DATE':
            if self.value_DATE_d is not None and self.value_DATE_m is not None and self.value_DATE_y is not None:
                date = str(self.value_DATE_y)+'-'+str(self.value_DATE_m)+'-'+str(self.value_DATE_d).zfill(2)
                pDate = parse_date(date)
                self.value_DATE = pDate
                self.value_STR = self.value_DATE.strftime('%d-%B-%Y').lstrip("0").replace(" 0", " ")
            elif self.value_DATE_m is not None and self.value_DATE_y is not None:
                self.value_STR = str(calendar.month_abbr[self.value_DATE_m])+'-'+str(self.value_DATE_y)
            elif self.value_DATE_y is not None:
                self.value_STR = str(self.value_DATE_y)
        super().save(*args, **kwargs)


class Concept(dalmeUuid):
    getty_id = models.IntegerField(db_index=True)
    tags = GenericRelation('Tag')


class Content_class(dalmeIntid):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Content_type(dalmeIntid):
    content_class = models.ForeignKey('Content_class', to_field='id', db_index=True, on_delete=models.PROTECT)
    name = models.CharField(max_length=255, unique=True)
    short_name = models.CharField(max_length=55)
    description = models.TextField()
    attribute_types = models.ManyToManyField(Attribute_type, through='Content_attributes')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class Content_attributes(dalmeIntid):
    content_type = models.ForeignKey('Content_type', to_field='id', db_index=True, on_delete=models.CASCADE, related_name='attribute_type_list')
    attribute_type = models.ForeignKey('Attribute_type', to_field='id', db_index=True, on_delete=models.CASCADE, related_name='content_types')
    order = models.IntegerField(db_index=True, null=True)
    required = models.BooleanField(default=False)


class DT_list(dalmeIntid):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55, unique=True)
    description = models.TextField(blank=True, default=None)
    content_types = models.ManyToManyField(Content_type)
    api_url = models.CharField(max_length=255, blank=True, default=None, null=True)
    helpers = models.CharField(max_length=255, blank=True, default=None, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']


class DT_fields(dalmeIntid):

    DTE_TYPES = (
        ('autoComplete', 'autoComplete'),
        ('checkbox', 'checkbox'),
        ('date', 'date'),
        ('datetime', 'datetime'),
        ('hidden', 'hidden'),
        ('password', 'password'),
        ('radio', 'radio'),
        ('readonly', 'readonly'),
        ('select', 'select'),
        ('selectize', 'selectize'),
        ('text', 'text'),
        ('textarea', 'textarea'),
        ('upload', 'upload'),
        ('uploadMany', 'uploadMany')
    )

    FILTER_TYPES = (
        ('check', 'check'),
        ('select', 'select'),
        ('switch', 'switch'),
        ('text', 'text'),
        ('date', 'date'),
        ('datetime', 'datetime'),
        ('integer', 'integer')
    )

    FILTER_OPERATORS = (
        ('and', 'and'),
        ('or', 'or')
    )

    list = models.ForeignKey('DT_list', to_field='id', db_index=True, on_delete=models.CASCADE, related_name='fields')
    field = models.ForeignKey('Attribute_type', to_field='id', db_index=True, on_delete=models.CASCADE)
    render_exp = models.CharField(max_length=255, null=True, default=None)
    orderable = models.BooleanField(default=False)
    visible = models.BooleanField(default=False)
    searchable = models.BooleanField(default=False)
    dt_name = models.CharField(max_length=55, null=True, default=None, blank=True)
    dt_class_name = models.CharField(max_length=255, null=True, default=None)
    dt_width = models.CharField(max_length=255, null=True, default=None)
    dte_name = models.CharField(max_length=55, null=True, default=None)
    dte_type = models.CharField(max_length=55, null=True, default=None, choices=DTE_TYPES)
    dte_options = models.CharField(max_length=255, null=True, default=None)
    dte_opts = models.CharField(max_length=255, null=True, default=None)
    dte_message = models.CharField(max_length=255, null=True, default=None)
    is_filter = models.BooleanField(default=False)
    filter_type = models.CharField(max_length=55, null=True, default=None, choices=FILTER_TYPES)
    filter_options = models.CharField(max_length=255, null=True, default=None)
    filter_lookup = models.CharField(max_length=255, null=True, default=None)
    order = models.IntegerField(db_index=True, null=True, default=None)

    def __str__(self):
        return self.field

    class Meta:
        unique_together = ("list", "field")
        ordering = ['order']


class Headword(dalmeUuid):
    word = models.CharField(max_length=55)
    full_lemma = models.CharField(max_length=255)
    concept_id = models.ForeignKey('Concept', to_field='id', db_index=True, on_delete=models.PROTECT)
    tags = GenericRelation('Tag')

    def __str__(self):
        return self.word


class Object(dalmeUuid):
    concept_id = models.UUIDField(db_index=True)
    object_phrase_id = models.ForeignKey('Object_phrase', to_field='id', db_index=True, on_delete=models.CASCADE)
    tags = GenericRelation('Tag')


class Object_attribute(dalmeBasic):
    object_id = models.ForeignKey('Object', to_field='id', db_index=True, on_delete=models.CASCADE)
    concept_id = models.UUIDField(db_index=True)


class Place(dalmeUuid):
    type = models.IntegerField(db_index=True)
    tags = GenericRelation('Tag')


class Page(dalmeUuid):
    name = models.CharField(max_length=55)
    dam_id = models.IntegerField(db_index=True, null=True)
    order = models.IntegerField(db_index=True)
    canvas = models.TextField(null=True)
    tags = GenericRelation('Tag')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('page_detail', kwargs={'pk': self.pk})

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
                "https://dam.dalme.org/iiif/{}/canvas/{}".format(self.dam_id, folio)
            )
            self.canvas = canvas.text
            return canvas.text
        else:
            return self.canvas


class Source_pages(dalmeIntid):
    source = models.ForeignKey('Source', to_field='id', db_index=True, on_delete=models.CASCADE)
    page = models.ForeignKey('Page', to_field='id', db_index=True, on_delete=models.CASCADE, related_name='sources')
    transcription = models.ForeignKey('Transcription', to_field='id', db_index=True, on_delete=models.SET_NULL, null=True)


class Source(dalmeUuid):
    type = models.ForeignKey('Content_type', to_field='id', db_index=True, on_delete=models.PROTECT, db_column="type")
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    is_inventory = models.BooleanField(default=False, db_index=True)
    attributes = GenericRelation(Attribute, related_query_name='sources')
    pages = models.ManyToManyField(Page, db_index=True, through='Source_pages')
    tags = GenericRelation('Tag')
    comments = GenericRelation('Comment')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('source_detail', kwargs={'pk': self.pk})


class Transcription(dalmeUuid):
    transcription = models.TextField(blank=True, default=None)
    author = models.CharField(max_length=255, default=get_current_username)
    version = models.IntegerField(null=True)

    def __str__(self):
        return str(self.id)


class Identity_phrase(dalmeUuid):
    transcription = models.ForeignKey('Transcription', to_field='id', db_index=True, on_delete=models.CASCADE)
    phrase = models.TextField()

    def __str__(self):
        return self.phrase


class Object_phrase(dalmeUuid):
    transcription = models.ForeignKey('Transcription', to_field='id', db_index=True, on_delete=models.CASCADE)
    phrase = models.TextField()

    def __str__(self):
        return self.phrase


class Wordform(dalmeUuid):
    normalized_form = models.CharField(max_length=55)
    pos = models.CharField(max_length=255)
    headword_id = models.ForeignKey('Headword', to_field='id', db_index=True, on_delete=models.PROTECT)
    tags = GenericRelation('Tag')

    def __str__(self):
        return self.normalized_form


class Token(dalmeUuid):
    object_phrase_id = models.ForeignKey('Object_phrase', to_field='id', db_index=True, on_delete=models.CASCADE)
    wordform_id = models.ForeignKey('Wordform', to_field='id', db_index=True, on_delete=models.PROTECT)
    raw_token = models.CharField(max_length=255)
    clean_token = models.CharField(max_length=55)
    order = models.IntegerField(db_index=True)
    flags = models.CharField(max_length=10)
    tags = GenericRelation('Tag')

    def __str__(self):
        return self.raw_token


class Identity_phrase_x_entity(dalmeBasic):
    identity_phrase_id = models.ForeignKey('Identity_phrase', to_field='id', db_index=True, on_delete=models.CASCADE)
    entity_id = models.UUIDField(db_index=True)

# app management models


class Country(dalmeIntid):
    name = models.CharField(max_length=255, unique=True)
    alpha_3_code = models.CharField(max_length=3)
    alpha_2_code = models.CharField(max_length=2)
    num_code = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class City(dalmeIntid):
    name = models.CharField(max_length=255)
    administrative_region = models.CharField(max_length=255)
    country = models.ForeignKey('Country', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name + '(' + self.country.name + ')'

    class Meta:
        ordering = ['country', 'name']
        unique_together = ("name", "administrative_region")


class Language(dalmeIntid):

    LANGUAGE_TYPES = (
        ('language', 'language'),
        ('dialect', 'dialect')
    )

    glottocode = models.CharField(max_length=25, unique=True)
    iso6393 = models.CharField(max_length=25, unique=True, blank=True, null=True, default=None)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=15, choices=LANGUAGE_TYPES)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name+' ('+self.glottocode+')'

    class Meta:
        ordering = ["name"]


class AttributeReference(dalmeUuid):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.TextField()
    data_type = models.CharField(max_length=15)
    source = models.CharField(max_length=255)
    term_type = models.CharField(max_length=55, blank=True, default=None)


class Workset(dalmeIntid):
    name = models.CharField(max_length=55)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=get_current_user)
    qset = models.TextField()
    endpoint = models.CharField(max_length=55)
    progress = models.FloatField(default=0)
    current_record = models.IntegerField(default=1)
    tags = GenericRelation('Tag')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        new_qset = json.loads(self.qset)
        done = sum(1 for value in new_qset.values() if 'done' in value)
        total = len(new_qset)
        self.progress = done * 100 / total
        super(Workset, self).save(*args, **kwargs)


class Tag(dalmeUuid):
    WORKFLOW = 'WF'  # type of tags used to keep track of general DALME workflow
    CONTROL = 'C'  # general purpose control tags
    TICKET = 'T'  # tags for issue ticket management
    TAG_TYPES = (
        (WORKFLOW, 'Workflow'),
        (CONTROL, 'Control'),
        (TICKET, 'Ticket')
    )
    TICKET_TAGS = (
        ('bug', 'bug'),
        ('feature', 'feature'),
        ('documentation', 'documentation'),
        ('question', 'question'),
        ('content', 'content')
    )

    tag_type = models.CharField(max_length=2, choices=TAG_TYPES)
    tag = models.CharField(max_length=55, null=True, default=None)
    tag_group = models.CharField(max_length=255, null=True, default=None)
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = object_id = models.CharField(max_length=55, null=True, db_index=True)

    def __str__(self):
        return self.tag

# task management


class TaskList(dalmeIntid):
    name = models.CharField(max_length=60)
    slug = models.SlugField(default="")
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="task_list_group")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Task Lists"
        # Prevents (at the database level) creation of two lists with the same slug in the same group
        unique_together = ("group", "slug")

    def save(self, **kwargs):
        self.slug = '_'.join(self.name.lower().split())
        super(TaskList, self).save()


class Task(dalmeIntid):
    title = models.CharField(max_length=140)
    task_list = models.ForeignKey(TaskList, on_delete=models.CASCADE, null=True)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="task_created_by", default=get_current_user)
    assigned_to = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="task_assigned_to")
    description = models.TextField(blank=True, null=True)
    priority = models.PositiveIntegerField(blank=True, null=True)
    workset = models.ForeignKey(Workset, on_delete=models.PROTECT, null=True)
    position = models.CharField(max_length=255, blank=True, default=None)
    url = models.CharField(max_length=255, null=True, default=None)
    file = models.ForeignKey('Attachment', blank=True, null=True, on_delete=models.SET_NULL)
    comments = GenericRelation('Comment', related_query_name='tasks')

    # Has due date for an instance of this object passed?
    def overdue_status(self):
        '''Returns whether the Tasks's due date has passed or not.'''
        if self.due_date and datetime.date.today() > self.due_date:
            return True

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("/tasks/", kwargs={"task_id": self.id})

    # Auto-set the Task creation / completed date
    def save(self, **kwargs):
        # If Task is being marked complete, set the completed_date
        if self.completed:
            self.completed_date = datetime.datetime.now()
        super(Task, self).save()

    class Meta:
        ordering = ["priority", "creation_timestamp"]


class Ticket(dalmeIntid):
    OPEN = 0
    CLOSED = 1
    STATUS = (
        (OPEN, 'Open'),
        (CLOSED, 'Closed')
    )

    subject = models.CharField(max_length=140)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=0)
    tags = GenericRelation('Tag')
    url = models.CharField(max_length=255, null=True, default=None)
    file = models.ForeignKey('Attachment', blank=True, null=True, on_delete=models.SET_NULL)
    comments = GenericRelation('Comment')

    @property
    def creation_name(self):
        return User.objects.get(username=self.creation_username).profile.full_name

    def __str__(self):
        return str(self.id) + ' - ' + self.title + ' ('+self.get_status_display+')'

    class Meta:
        ordering = ["status", "creation_timestamp"]


class Comment(dalmeIntid):
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.CharField(max_length=55, null=True, db_index=True)
    body = models.TextField(blank=True, null=True, default=None)

    @property
    def snippet(self):
        body_snippet = textwrap.shorten(self.body, width=35, placeholder="...")
        return "{author} - {snippet}...".format(author=self.creation_username, snippet=body_snippet)

    def __str__(self):
        return self.snippet


class Attachment(dalmeUuid):
    file = models.FileField(upload_to='attachments/%Y/%m/')
    type = models.CharField(max_length=255, null=True)

    @property
    def filename(self):
        return os.path.basename(self.file.name)

    def extension(self):
        name, extension = os.path.splitext(self.file.name)
        return extension

    def preview(self):
        icon_type_dict = {
            'application/msword': 'fa-file-word',
            'text/csv': 'fa-file-csv',
            'application/pdf': 'fa-file-pdf',
            'application/zip': 'fa-file-archive',
            'application/vnd.ms-excel': 'fa-file-excel'
        }
        icon_class_dict = {
            'audio': 'fa-file-audio',
            'video': 'fa-file-video',
            'image': 'fa-file-image',
            'text': 'fa-file-alt',
        }
        if icon_type_dict.get(self.type) is not None:
            icon = icon_type_dict.get(self.type)
        elif icon_class_dict.get(self.type.split('/')[0]) is not None:
            icon = icon_class_dict.get(self.type.split('/')[0])
        else:
            icon = 'fa-file'
        if self.type.split('/')[0] == 'image':
            preview = '<div class="attachment-file"><div class="attachment-file-body"><img src="{}" class="attachment-file-image" alt="image">\
                                   </div><div class="attachment-file-label">{}</div></div>'.format('/media/'+str(self.file), self.filename)
        else:
            preview = '<div class="attachment-file"><div class="attachment-file-body"><i class="far {} fa-8x"></i>\
                                   </div><div class="attachment-file-label"><a href="/download/{}">{}</a></div>\
                                   </div>'.format(icon, self.file, self.filename)
        return preview

    def __str__(self):
        return self.file.name

    def save(self, *args, **kwargs):
        type, encoding = mimetypes.guess_type(str(self.file).split('/').pop(-1))
        self.type = type
        super(Attachment, self).save(*args, **kwargs)

# unmanaged models from DAM


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
    country = models.CharField(max_length=200, null=True, default=None)
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
    geo_lat = models.FloatField(null=True, default=None)
    geo_long = models.FloatField(null=True, default=None)
    mapzoom = models.IntegerField(null=True)
    disk_usage = models.IntegerField(null=True)
    disk_usage_last_updated = models.DateTimeField(null=True, blank=True)
    file_size = models.IntegerField(null=True, default=None)
    preview_attempts = models.IntegerField(null=True, default=None)
    field12 = models.CharField(max_length=200, null=True, default=None)
    field8 = models.CharField(max_length=200, null=True, default=None)
    field3 = models.CharField(max_length=200, null=True, default=None)
    annotation_count = models.IntegerField(null=True)
    field51 = models.CharField(max_length=200, null=True, default=None)
    field79 = models.CharField(max_length=200, null=True, default=None, blank=True)
    modified = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    collections = models.ManyToManyField('rs_collection', through='rs_collection_resource')

    class Meta:
        managed = False
        db_table = 'resource'
        in_db = 'dam'


class rs_resource_data(models.Model):
    django_id = models.IntegerField(primary_key=True, db_column="django_id")
    resource = models.ForeignKey('rs_resource', db_column="resource", to_field='ref', on_delete=models.CASCADE, related_name='resource_data')
    resource_type_field = models.ForeignKey('rs_resource_type_field', db_column="resource_type_field", to_field='ref', on_delete=models.CASCADE, related_name='resource_data_field')
    value = models.TextField()

    class Meta:
        managed = False
        db_table = 'resource_data'
        in_db = 'dam'


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
        managed = False
        db_table = 'collection'
        in_db = 'dam'


class rs_collection_resource(models.Model):
    collection = models.ForeignKey('rs_collection', db_column="collection", to_field='ref', on_delete=models.CASCADE, related_name='resources_list')
    resource = models.ForeignKey('rs_resource', db_column="resource", to_field='ref', on_delete=models.CASCADE, related_name='collections_list')
    date_added = models.DateTimeField(auto_now_add=True, primary_key=True)
    comment = models.TextField()
    rating = models.IntegerField(null=True)
    use_as_theme_thumbnail = models.IntegerField(null=True)
    purchase_size = models.CharField(max_length=10, null=True)
    purchase_complete = models.IntegerField(default='0')
    purchase_price = models.FloatField(max_length=10, default='0.00')
    sortorder = models.IntegerField(null=True)

    class Meta:
        managed = False
        db_table = 'collection_resource'
        in_db = 'dam'


class rs_user(models.Model):

    DAM_USERGROUPS = (
        (2, 'General User'),
        (4, 'Archivist'),
        (1, 'Administrator'),
        (3, 'Super Admin'),
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
        managed = False
        db_table = 'user'
        in_db = 'dam'


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
        managed = False
        db_table = 'resource_type_field'
        in_db = 'dam'

# unmanaged models from WIKI


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
        managed = False
        db_table = 'user'
        in_db = 'wiki'


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
        managed = False
        db_table = 'user_groups'
        in_db = 'wiki'


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
        managed = False
        db_table = 'page'
        in_db = 'wiki'


# unmanaged models from WORDPRESS
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
        managed = False
        db_table = 'wp_users'
        in_db = 'wp'


class wp_usermeta(models.Model):
    umeta_id = models.IntegerField(primary_key=True)
    user_id = models.IntegerField(default='0')
    meta_key = models.CharField(max_length=255, null=True)
    meta_value = models.TextField()

    class Meta:
        managed = False
        db_table = 'wp_usermeta'
        in_db = 'wp'
