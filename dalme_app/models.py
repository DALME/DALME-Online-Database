from django.contrib.auth.models import User, Group
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from dalme_app.utils import get_current_user, get_current_username
import os
import json
import requests
import hashlib
import textwrap
import xml.etree.ElementTree as et
from urllib.parse import urlencode
import datetime
from dalme_app.model_templates import dalmeBasic, dalmeUuid, dalmeIntid
import django.db.models.options as options
from django.utils.dateparse import parse_date
from django.utils import timezone
import calendar
import mimetypes
import uuid
# from django.conf import settings
from django.dispatch import receiver
from collections import Counter

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


def rs_api_query(endpoint, user, key, **kwargs):
    sign = hashlib.sha256(key.encode('utf-8'))
    paramDict = kwargs
    paramDict['user'] = user
    paramstr = urlencode(paramDict)
    sign.update(paramstr.encode('utf-8'))
    R = requests.get(endpoint + paramstr + "&sign=" + sign.hexdigest())
    return R


# ->**************************************    DATA STORE   **************************************

# ->Content and Attributes
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
    attribute_types = models.ManyToManyField('Attribute_type', through='Content_attributes')
    has_pages = models.BooleanField(default=False, db_index=True)
    has_inventory = models.BooleanField(default=False)
    parents = models.CharField(max_length=255, blank=True, default=None, null=True)
    r1_inheritance = models.CharField(max_length=255, blank=True, default=None, null=True)
    r2_inheritance = models.CharField(max_length=255, blank=True, default=None, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']

    @property
    def inheritance(self):
        inheritance = {}
        if self.r1_inheritance:
            inheritance['r1'] = self.r1_inheritance.split(',')
        if self.r2_inheritance:
            inheritance['r2'] = self.r2_inheritance.split(',')
        return inheritance


class Attribute_type(dalmeIntid):

    DATA_TYPES = (
        ('DATE', 'DATE (date)'),
        ('INT', 'INT (integer)'),
        ('STR', 'STR (string)'),
        ('TXT', 'TXT (text)'),
        ('UUID', 'UUID (DALME record)')
    )

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55, unique=True)
    description = models.TextField()
    data_type = models.CharField(max_length=15, choices=DATA_TYPES)
    source = models.CharField(max_length=255, blank=True, null=True, default=None)
    same_as = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, db_column="same_as")
    options_list = models.CharField(max_length=255, blank=True, null=True, default=None)

    def __str__(self):
        # return self.name + ' ('+self.short_name+')'
        return self.name

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
        elif self.attribute_type.data_type == 'UUID':
            val_data = json.loads(self.value_STR)
            object = eval('{}.objects.get(pk="{}")'.format(val_data['class'], val_data['id']))
            str_val = '<a href="{}">{}</a>'.format(object.get_url(), object.name)
        else:
            str_val = str(eval('self.value_' + self.attribute_type.data_type))
        return str_val

    def save(self, *args, **kwargs):
        if self.attribute_type.data_type == 'DATE':
            if self.value_DATE_d is not None and self.value_DATE_m is not None and self.value_DATE_y is not None:
                date = str(self.value_DATE_y)+'-'+str(self.value_DATE_m)+'-'+str(self.value_DATE_d).zfill(2)
                pDate = parse_date(date)
                self.value_DATE = pDate
                self.value_STR = self.value_DATE.strftime('%d-%b-%Y').lstrip("0").replace(" 0", " ")
            elif self.value_DATE_m is not None and self.value_DATE_y is not None:
                self.value_STR = str(calendar.month_abbr[self.value_DATE_m])+'-'+str(self.value_DATE_y)
            elif self.value_DATE_y is not None:
                self.value_STR = str(self.value_DATE_y)
        super().save(*args, **kwargs)


class Content_attributes(dalmeIntid):
    content_type = models.ForeignKey('Content_type', to_field='id', db_index=True, on_delete=models.CASCADE, related_name='attribute_type_list')
    attribute_type = models.ForeignKey('Attribute_type', to_field='id', db_index=True, on_delete=models.CASCADE, related_name='content_types')
    order = models.IntegerField(db_index=True, null=True)
    required = models.BooleanField(default=False)
# <-


# -> Source Management
class Source(dalmeUuid):
    type = models.ForeignKey('Content_type', to_field='id', db_index=True, on_delete=models.PROTECT, db_column="type")
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)
    has_inventory = models.BooleanField(default=False, db_index=True)
    attributes = GenericRelation('Attribute', related_query_name='sources')
    pages = models.ManyToManyField('Page', db_index=True, through='Source_pages')
    tags = GenericRelation('Tag')
    comments = GenericRelation('Comment')
    sets = GenericRelation('Set_x_content', related_query_name='source')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('source_detail', kwargs={'pk': self.pk})

    @property
    def is_public(self):
        try:
            return self.workflow.is_public
        except Workflow.DoesNotExist:
            return False

    @property
    def inherited(self):
        inheritance = self.type.inheritance
        if self.parent and inheritance.get('r1', None) is not None:
            r1_inherited = self.parent.attributes.filter(attribute_type__in=inheritance['r1'])
            if self.parent.parent and inheritance.get('r2', None) is not None:
                r2_inherited = self.parent.inherited.filter(attribute_type__in=inheritance['r2'])
                return r1_inherited | r2_inherited
            else:
                return r1_inherited

    @property
    def agents(self):
        ep_list = [i.transcription.entity_phrases.filter(content_type=104) for i in self.source_pages.all().select_related('transcription') if i.transcription]
        if len(ep_list) > 0:
            return [i.content_object for i in ep_list[0].union(*ep_list[1:])]

    @property
    def places(self):
        ep_list = [i.transcription.entity_phrases.filter(content_type=115) for i in self.source_pages.all().select_related('transcription') if i.transcription]
        if len(ep_list) > 0:
            return [i.content_object for i in ep_list[0].union(*ep_list[1:])]

    @property
    def objects(self):
        ep_list = [i.transcription.entity_phrases.filter(content_type=118) for i in self.source_pages.all().select_related('transcription') if i.transcription]
        if len(ep_list) > 0:
            return [i.content_object for i in ep_list[0].union(*ep_list[1:])]

    @property
    def has_images(self):
        if self.pages.exclude(dam_id__isnull=True).count() > 0:
            return True
        else:
            return False

    @property
    def no_folios(self):
        if self.pages.all().exists():
            return self.pages.all().count()
        else:
            return 0

    @property
    def no_transcriptions(self):
        if self.source_pages.exclude(transcription__count_ignore=True).exists():
            return self.source_pages.exclude(transcription__count_ignore=True).count()
        else:
            return 0

    @property
    def has_transcriptions(self):
        if self.source_pages.all().select_related('transcription').exists():
            return True
        else:
            return False

    @property
    def get_credit_line(self):
        try:
            editor = User.objects.get(username=self.creation_username).profile.full_name
            contributors = [i.user.profile.full_name for i in self.workflow.work_log.all()]
            tr_cr = [User.objects.get(username=i.creation_username).profile.full_name for i in self.source_pages.all().select_related('transcription')]
            contributors = contributors + tr_cr
            tr_mod = [User.objects.get(username=i.modification_username).profile.full_name for i in self.source_pages.all().select_related('transcription')]
            contributors = contributors + tr_mod
            contributors = [i for i in contributors if i != editor]
            if len(contributors) == 0:
                credit_line = 'Edited by {}.'.format(editor)
            elif len(contributors) == 1:
                credit_line = 'Edited by {}, with contributions by {}.'.format(editor, contributors[0])
            else:
                contributors_list = "{}, and {}".format(", ".join(contributors[:-1]),  contributors[-1])
                credit_line = 'Edited by {}, with contributions by {}.'.format(editor, contributors_list)
            return credit_line
        except Exception as e:
            return str(e)


@receiver(models.signals.post_save, sender=Source)
def update_workflow(sender, instance, created, **kwargs):
    if instance.has_inventory:
        if created:
            wf_object = Workflow.objects.create(source=instance, last_modified=instance.modification_timestamp)
            Work_log.objects.create(source=wf_object, event='Source created', timestamp=wf_object.last_modified)
        else:
            wf_object = Workflow.objects.get(pk=instance.id)
            wf_object.last_modified = timezone.now()
            wf_object.last_user = get_current_user()
            wf_object.save()


@receiver(models.signals.pre_delete, sender=Source)
def delete_source_dependencies(sender, instance, **kwargs):
    if instance.pages:
        for page in instance.pages.all():
            if page.sources:
                for sp in page.sources.all():
                    if sp.transcription:
                        sp.transcription.delete()
            page.delete()


class Page(dalmeUuid):
    name = models.CharField(max_length=55)
    dam_id = models.IntegerField(db_index=True, null=True)
    order = models.IntegerField(db_index=True)
    canvas = models.TextField(null=True)
    tags = GenericRelation('Tag')

    def __str__(self):
        return self.name

    def get_rights(self):
        if self.sources.all()[0].source.parent.parent.attributes.filter(attribute_type=144).exists():
            rpo = RightsPolicy.objects.get(pk=json.loads(self.sources.all()[0].source.parent.parent.attributes.get(attribute_type=144).value_STR)['id'])
            return {'status': rpo.get_rights_status_display(), 'display_notice': rpo.notice_display, 'notice': json.loads(rpo.rights_notice)}

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


@receiver(models.signals.post_save, sender=Page)
def update_folio(sender, instance, created, **kwargs):
    if created:
        rs_image = rs_resource.objects.get(ref=instance.dam_id)
        rs_image.field79 = instance.name
        rs_image.save()


class Source_pages(dalmeIntid):
    source = models.ForeignKey('Source', to_field='id', db_index=True, on_delete=models.CASCADE,  related_name='source_pages')
    page = models.ForeignKey('Page', to_field='id', db_index=True, on_delete=models.CASCADE, related_name='sources')
    transcription = models.ForeignKey('Transcription', to_field='id', db_index=True, on_delete=models.SET_NULL, null=True, related_name='source_pages')


class Transcription(dalmeUuid):
    transcription = models.TextField(blank=True, default=None)
    author = models.CharField(max_length=255, default=get_current_username)
    version = models.IntegerField(null=True)
    count_ignore = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    def save(self, **kwargs):
        # set count_ignore flag
        tr_tree = et.fromstring('<xml>' + self.transcription + '</xml>')
        if len(tr_tree) == 1 and tr_tree[0].tag in ['quote', 'gap', 'mute'] or len(tr_tree) == 0:
            self.count_ignore = True
        super(Task, self).save()


@receiver(models.signals.post_save, sender=Transcription)
def update_source_modification(sender, instance, created, **kwargs):
    if instance.source_pages.all().exists():
        source_id = instance.source_pages.all().first().source.id
        source = Source.objects.get(pk=source_id)
        source.modification_timestamp = timezone.now()
        source.modification_username = get_current_username()
        source.save()


class Entity_phrase(dalmeUuid):
    AGENT = 1
    OBJECT = 2
    PLACE = 3
    ENTITY_TYPES = (
        (AGENT, 'Agent'),
        (OBJECT, 'Object'),
        (PLACE, 'Place'),
    )

    phrase = models.TextField(blank=True)
    type = models.IntegerField(choices=ENTITY_TYPES)
    transcription_id = models.ForeignKey('Transcription', to_field='id', db_index=True, on_delete=models.CASCADE, related_name='entity_phrases')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.UUIDField(null=True, db_index=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.phrase
# <-


# -> Entities and Relationships
class Agent(dalmeUuid):
    PERSON = 1
    ORGANIZATION = 2
    AGENT_TYPES = (
        (PERSON, 'Person'),
        (ORGANIZATION, 'Organization'),
    )

    std_name = models.CharField(max_length=255)
    type = models.IntegerField(choices=AGENT_TYPES)
    attributes = GenericRelation('Attribute')
    instances = GenericRelation('Entity_phrase')
    relations = GenericRelation('Relationship', content_type_field='source_content_type', object_id_field='source_object_id')
    notes = models.TextField()
    tags = GenericRelation('Tag')


class Object(dalmeUuid):
    concept = models.ForeignKey('Concept', db_index=True, on_delete=models.CASCADE)
    instances = GenericRelation('Entity_phrase')
    tags = GenericRelation('Tag')


class Object_attribute(dalmeUuid):
    object = models.ForeignKey('Object', db_index=True, on_delete=models.CASCADE)
    attribute_concept = models.ForeignKey('Concept', db_index=True, on_delete=models.CASCADE)


class Place(dalmeUuid):
    std_name = models.CharField(max_length=255)
    type = models.IntegerField(db_index=True)
    attributes = GenericRelation('Attribute')
    instances = GenericRelation('Entity_phrase')
    tags = GenericRelation('Tag')


class Relationship(dalmeUuid):
    source_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, related_name='relationship_sources')
    source_object_id = models.UUIDField(null=True, db_index=True)
    source_object = GenericForeignKey('source_content_type', 'source_object_id')
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, related_name='relationship_targets')
    target_object_id = models.UUIDField(null=True, db_index=True)
    target_object = GenericForeignKey('target_content_type', 'target_object_id')
    attributes = GenericRelation('Attribute')
    scope = models.ForeignKey('Scope', on_delete=models.CASCADE, null=True)
    notes = models.TextField(blank=True)


class Scope(dalmeUuid):
    TEMPORAL = 1  # relationship applies only during a certain timeframe. Defined by start and end dates, start + duration, ...
    SPATIAL = 2  # relationship applies only within a certain spatial/geographical area. Defined by place id (e.g. a house, a city, a country), shapefile, polygon geometry, ...
    LINGUISTIC = 3  # relationship applies only for a language or dialect. Defined by language id.
    CONTEXT = 4  # relationship applies only in a context identified by a DALME id (e.g. a source or a page)
    SCOPE_TYPES = (
        (TEMPORAL, 'Temporal'),
        (SPATIAL, 'Spatial'),
        (LINGUISTIC, 'Linguistic'),
        (CONTEXT, 'Context')
    )

    type = models.IntegerField(choices=SCOPE_TYPES)
    range = models.TextField()  # a JSON object that contains the scope parameters, depending on its type
# <-


# -> Language Processing
class Concept(dalmeUuid):
    getty_id = models.IntegerField(db_index=True)
    tags = GenericRelation('Tag')


class Headword(dalmeUuid):
    word = models.CharField(max_length=55)
    full_lemma = models.CharField(max_length=255)
    concept_id = models.ForeignKey('Concept', to_field='id', db_index=True, on_delete=models.PROTECT)
    tags = GenericRelation('Tag')

    def __str__(self):
        return self.word


class Token(dalmeUuid):
    object_phrase_id = models.ForeignKey('Entity_phrase', to_field='id', db_index=True, on_delete=models.CASCADE)
    wordform_id = models.ForeignKey('Wordform', to_field='id', db_index=True, on_delete=models.PROTECT)
    raw_token = models.CharField(max_length=255)
    clean_token = models.CharField(max_length=55)
    order = models.IntegerField(db_index=True)
    flags = models.CharField(max_length=10)
    tags = GenericRelation('Tag')

    def __str__(self):
        return self.raw_token


class Wordform(dalmeUuid):
    normalized_form = models.CharField(max_length=55)
    pos = models.CharField(max_length=255)
    headword_id = models.ForeignKey('Headword', to_field='id', db_index=True, on_delete=models.PROTECT)
    tags = GenericRelation('Tag')

    def __str__(self):
        return self.normalized_form
# <-


# ->User Profiles and Sets
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


class Set(dalmeUuid):
    CORPUS = 1  # a set representing a coherent body of materials defined by a project or sub-project
    COLLECTION = 2  # a generic set defined by a user for any purpose -- collections could potentially by qualified by other terms
    DATASET = 3  # a set defined for analytical purposes
    WORKSET = 4  # a set defined as part of a project's workflow for the purpose of systematically performing a well-defined task to its members
    PRIVATE = 1  # only owner can view set
    VIEW = 2  # others can view the set
    ADD = 3  # others can view the set and add members
    DELETE = 4  # others can view the set and add and delete members
    SET_TYPES = (
        (CORPUS, 'Corpus'),
        (COLLECTION, 'Collection'),
        (DATASET, 'Dataset'),
        (WORKSET, 'Workset')
    )
    SET_PERMISSIONS = [
        (PRIVATE, 'Private'),
        (VIEW, 'Others: view'),
        (ADD, 'Others: view|add'),
        (DELETE, 'Others: view|add|delete')
    ]

    name = models.CharField(max_length=255)
    set_type = models.IntegerField(choices=SET_TYPES)
    is_public = models.BooleanField(default=False)
    has_landing = models.BooleanField(default=False)
    endpoint = models.CharField(max_length=55)
    owner_local = models.ForeignKey(User, on_delete=models.CASCADE, default=get_current_user)
    set_permissions = models.IntegerField(choices=SET_PERMISSIONS, default=VIEW)
    description = models.TextField()
    comments = GenericRelation('Comment')
    stat_title = models.CharField(max_length=25, null=True)
    stat_text = models.CharField(max_length=255, null=True)

    def __str__(self):
        return f'{self.name}({self.set_type})'

    @property
    def workset_progress(self):
        done = self.members.filter(workset_done=True).count()
        total = self.members.count()
        if total != 0:
            return done * 100 / total
        else:
            return 0

    @property
    def get_member_count(self):
        return self.members.count()

    @property
    def get_public_member_count(self):
        return self.members.filter(source__workflow__is_public=True).count()

    @property
    def get_languages(self):
        return [[LanguageReference.objects.get(iso6393=i).name, i] for i in set(self.members.filter(source__attributes__attribute_type=15).values_list('source__attributes__value_STR', flat=True))]

    @property
    def get_public_languages(self):
        return [[LanguageReference.objects.get(iso6393=i).name, i] for i in set(self.members.filter(source__attributes__attribute_type=15, source__workflow__is_public=True).values_list('source__attributes__value_STR', flat=True))]

    @property
    def get_time_coverage(self):
        years = self.members.filter(source__attributes__attribute_type=26).order_by('source__attributes__value_DATE_y').values_list('source__attributes__value_DATE_y', flat=True)
        return dict(Counter(years))

    @property
    def get_public_time_coverage(self):
        years = self.members.filter(source__attributes__attribute_type=26, source__workflow__is_public=True).order_by('source__attributes__value_DATE_y').values_list('source__attributes__value_DATE_y', flat=True)
        return dict(Counter(years))


class Set_x_content(dalmeBasic):
    set_id = models.ForeignKey(Set, on_delete=models.CASCADE, related_name='members')
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.UUIDField(default=uuid.uuid4, db_index=True)
    workset_done = models.BooleanField(default=False)

    class Meta:
        unique_together = ('content_type', 'object_id', 'set_id')
        ordering = ['set_id', 'id']


# <-
# <-

# ->**************************************    REFERENCE DATASETS    **************************************


class AttributeReference(dalmeUuid):
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    description = models.TextField()
    data_type = models.CharField(max_length=15)
    source = models.CharField(max_length=255)
    term_type = models.CharField(max_length=55, blank=True, default=None)


class CityReference(dalmeIntid):
    name = models.CharField(max_length=255)
    administrative_region = models.CharField(max_length=255)
    country = models.ForeignKey('CountryReference', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.name}({self.country.name})'

    class Meta:
        ordering = ['country', 'name']
        unique_together = ('name', 'administrative_region')


class CountryReference(dalmeIntid):
    name = models.CharField(max_length=255, unique=True)
    alpha_3_code = models.CharField(max_length=3)
    alpha_2_code = models.CharField(max_length=2)
    num_code = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class LanguageReference(dalmeIntid):
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
# <-

# ->**************************************    APPLICATION MANAGEMENT    **************************************


# -> Workflow
class Workflow(models.Model):
    ASSESSING = 1
    PROCESSING = 2
    DONE = 3
    INGESTION = 1
    TRANSCRIPTION = 2
    MARKUP = 3
    REVIEW = 4
    PARSING = 5
    WORKFLOW_STATUS = (
        (ASSESSING, 'assessing'),
        (PROCESSING, 'processing'),
        (DONE, 'processed')
    )
    PROCESSING_STAGES = (
        (INGESTION, 'ingestion'),
        (TRANSCRIPTION, 'transcription'),
        (MARKUP, 'markup'),
        (REVIEW, 'review'),
        (PARSING, 'parsing')
    )

    source = models.OneToOneField(Source, on_delete=models.CASCADE, related_name='workflow', primary_key=True)
    wf_status = models.IntegerField(choices=WORKFLOW_STATUS, default=2)
    stage = models.IntegerField(choices=PROCESSING_STAGES, default=1)
    last_modified = models.DateTimeField(null=True, blank=True)
    last_user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, default=get_current_user)
    help_flag = models.BooleanField(default=False)
    ingestion_done = models.BooleanField(default=False)
    transcription_done = models.BooleanField(default=False)
    markup_done = models.BooleanField(default=False)
    parsing_done = models.BooleanField(default=False)
    review_done = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)

    @property
    def status(self):
        stage_dict = dict(self.PROCESSING_STAGES)
        if 1 <= self.wf_status <= 3:
            if self.wf_status != 2:
                status_text = self.get_wf_status_display()
                status_text_alt = ''
                css_class = 'tag-wf-' + status_text
            else:
                if getattr(self, self.get_stage_display() + '_done'):
                    status_text = 'awaiting ' + stage_dict[self.stage + 1]
                    status_text_alt = 'begin ' + stage_dict[self.stage + 1]
                    css_class = 'tag-wf-awaiting'
                else:
                    status_text = self.get_stage_display() + ' in progress'
                    status_text_alt = ''
                    css_class = 'tag-wf-in_progress'
        else:
            status_text = 'unknown'
            status_text_alt = ''
            css_class = 'tag-wf-unknown'
        return {'text': status_text, 'css_class': css_class, 'text_alt': status_text_alt}

    @property
    def stage_done(self):
        if self.wf_status == 2:
            stage_done = getattr(self, self.get_stage_display() + '_done')
        else:
            stage_done = True
        return stage_done


class Work_log(models.Model):
    id = models.AutoField(primary_key=True, unique=True, db_index=True)
    source = models.ForeignKey('Workflow', db_index=True, on_delete=models.CASCADE, related_name="work_log")
    event = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, default=get_current_user)
# <-


# ->Tasks and Tickets
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
            preview = '<div class="attachment-file"><img src="{}" class="attachment-file-image" alt="image">\
                                   <div class="attachment-file-label">{}</div></div>'.format('https://dalme-app-media.s3.amazonaws.com/media/'+str(self.file), self.filename)
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


class Task(dalmeIntid):
    title = models.CharField(max_length=140)
    task_list = models.ForeignKey('TaskList', on_delete=models.CASCADE)
    due_date = models.DateField(blank=True, null=True)
    completed = models.BooleanField(default=False)
    completed_date = models.DateField(blank=True, null=True)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="task_created_by", default=get_current_user)
    assigned_to = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name="task_assigned_to")
    description = models.TextField(blank=True, null=True)
    priority = models.PositiveIntegerField(blank=True, null=True)
    workset = models.ForeignKey('Set', on_delete=models.PROTECT, null=True)
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
# <-


# ->Data annotation: Comments, Tags, Rights
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

    class Meta:
        ordering = ['creation_timestamp']


class RightsPolicy(dalmeUuid):
    COPYRIGHTED = 1
    ORPHANED = 2
    OWNED = 3
    PUBLIC_DOMAIN = 4
    UNKNOWN = 5
    RIGHTS_STATUS = (
        (COPYRIGHTED, 'Copyrighted'),
        (ORPHANED, 'Orphaned'),
        (OWNED, 'Owned'),
        (PUBLIC_DOMAIN, 'Public Domain'),
        (UNKNOWN, 'Unknown'),
    )
    name = models.CharField(max_length=100)
    rights_status = models.IntegerField(choices=RIGHTS_STATUS, default=5)
    rights = models.TextField(blank=True, default=None)
    rights_notice = models.TextField(blank=True, default=None)
    licence = models.TextField(blank=True, null=True, default=None)
    rights_holder = models.CharField(max_length=255, null=True, default=None)
    notice_display = models.BooleanField(default=False)
    attachments = models.ForeignKey('Attachment', blank=True, null=True, on_delete=models.SET_NULL)
    comments = GenericRelation('Comment')

    def get_url(self):
        return '/rights/' + str(self.id)


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
    object_id = models.CharField(max_length=55, null=True, db_index=True)

    def __str__(self):
        return self.tag
# <


# -> DataTables
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
# <-
# <-

# ->**************************************    EXTERNAL UNMANAGED MODELS    **************************************


# -> ResourceSpace
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
# <-


# -> MediaWiki
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
# <-


# -> Wordpress
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
# <-
# <-
