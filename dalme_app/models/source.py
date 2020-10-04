from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
import lxml.etree as et
from dalme_app.models._templates import dalmeIntid, dalmeUuid, dalmeUuidOwned
import django.db.models.options as options
from wagtail.search import index
from dalme_app.models.workflow import Workflow

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class Source(index.Indexed, dalmeUuidOwned):
    type = models.ForeignKey('Content_type', to_field='id', db_index=True, on_delete=models.PROTECT, db_column="type")
    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, related_name='children')
    has_inventory = models.BooleanField(default=False, db_index=True)
    attributes = GenericRelation('Attribute', related_query_name='sources')
    pages = models.ManyToManyField('Page', db_index=True, through='Source_pages')
    tags = GenericRelation('Tag')
    comments = GenericRelation('Comment')
    sets = GenericRelation('Set_x_content', related_query_name='source')
    primary_dataset = models.ForeignKey('Set', db_index=True, on_delete=models.PROTECT, related_query_name='set_members', null=True)
    is_private = models.BooleanField(default=False, db_index=True)

    search_fields = [
        index.FilterField('name'),
    ]

    class Meta:
        unique_together = ('type', 'name')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.type.id == 13 and self.parent is not None:
            if self.parent.primary_dataset is not None:
                self.primary_dataset = self.parent.primary_dataset
        super().save(*args, **kwargs)

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
        if self.parent and inheritance.get('r1') is not None:
            r1_inherited = self.parent.attributes.filter(attribute_type__in=inheritance['r1'])
            if self.parent.parent and inheritance.get('r2') is not None:
                r2_inherited = self.parent.inherited.filter(attribute_type__in=inheritance['r2'])
                return r1_inherited | r2_inherited
            else:
                return r1_inherited

    def agents(self):
        ep_list = [i.transcription.entity_phrases.filter(content_type=104) for i in self.source_pages.all().select_related('transcription') if i.transcription]
        if len(ep_list) > 0:
            return [i.content_object for i in ep_list[0].union(*ep_list[1:])]

    def places(self):
        ep_list = [i.transcription.entity_phrases.filter(content_type=115) for i in self.source_pages.all().select_related('transcription') if i.transcription]
        if len(ep_list) > 0:
            return [i.content_object for i in ep_list[0].union(*ep_list[1:])]

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
    def no_images(self):
        if self.pages.exclude(dam_id__isnull=True).exists():
            return self.pages.exclude(dam_id__isnull=True).count()
        else:
            return 0

    @property
    def no_records(self):
        return self.children.count()

    @property
    def has_transcriptions(self):
        if self.source_pages.all().select_related('transcription').exists():
            return True
        else:
            return False

    @property
    def no_transcriptions(self):
        if self.source_pages.exclude(transcription__count_ignore=True).exists():
            return self.source_pages.exclude(transcription__count_ignore=True).count()
        else:
            return 0

    @property
    def no_folios(self):
        if self.pages.all().exists():
            return self.pages.all().count()
        else:
            return 0

    def get_credit_line(self):
        try:
            editor = self.owner.profile.full_name
            contributors = [i.user.profile.full_name for i in self.workflow.work_log.all()]
            tr_cr = [i.creation_user.profile.full_name for i in self.source_pages.all().select_related('transcription')]
            contributors = contributors + tr_cr
            tr_mod = [i.modification_user.profile.full_name for i in self.source_pages.all().select_related('transcription')]
            contributors = list(set(contributors + tr_mod))
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

    def get_transcription_blob(self):
        if self.source_pages.all().select_related('transcription').exists():
            trs = self.source_pages.all().select_related('transcription')
            text = ''
            xml_parser = et.XMLParser(recover=True)
            for tr in trs:
                try:
                    tr_tree = et.fromstring('<xml>' + tr.transcription.transcription + '</xml>', xml_parser)
                    txt_tr = et.tostring(tr_tree, encoding='utf8', method='text').decode('utf-8')
                    text = text + txt_tr
                except: # NOQA
                    continue
            return text

    def get_attribute_blob(self):
        att_blob = {}
        for att in self.attributes.all():
            att_blob[att.attribute_type.name] = att.value_STR
        return str(att_blob)

    def get_data_blob(self):
        return str(self.get_attribute_blob()) + str(self.get_transcription_blob())


class Source_credit(dalmeUuid):
    EDITOR = 1
    CORRECTIONS = 2
    CONTRIBUTOR = 3
    CREDIT_TYPES = (
        (EDITOR, 'Editor'),
        (CORRECTIONS, 'Corrections'),
        (CONTRIBUTOR, 'Contributor'),
    )

    source = models.ForeignKey('Source', to_field='id', db_index=True, on_delete=models.CASCADE, related_name='credits')
    agent = models.ForeignKey('Agent', to_field='id', db_index=True, on_delete=models.CASCADE, related_name='credits')
    type = models.IntegerField(choices=CREDIT_TYPES)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('source', 'agent', 'type')


class Source_pages(dalmeIntid):
    source = models.ForeignKey('Source', to_field='id', db_index=True, on_delete=models.CASCADE, related_name='source_pages')
    page = models.ForeignKey('Page', to_field='id', db_index=True, on_delete=models.CASCADE, related_name='sources')
    transcription = models.ForeignKey('Transcription', to_field='id', db_index=True, on_delete=models.SET_NULL, null=True, related_name='source_pages')
