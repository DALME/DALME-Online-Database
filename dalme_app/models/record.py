from wagtail.search import index

from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import options
from django.urls import reverse

from dalme_app.models.templates import dalmeIntid, dalmeOwned, dalmeUuid
from dalme_app.models.workflow import Workflow

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class RecordGroup(dalmeUuid, dalmeOwned):
    """Stores information about archival units."""

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    parent = GenericForeignKey('parent_type', 'parent_id')
    parent_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    parent_id = models.CharField(max_length=36, db_index=True, null=True)  # noqa: DJ001
    attributes = GenericRelation('Attribute', related_query_name='record_group')
    children = GenericRelation('Record', related_query_name='record_group')
    permissions = GenericRelation('Permission', related_query_name='record_group')
    tags = GenericRelation('Tag')
    comments = GenericRelation('Comment')

    @property
    def comment_count(self):
        """Return count of comments."""
        return self.comments.count()

    @property
    def is_private(self):
        """Return boolean indicating whether the record is private."""
        if self.permissions.filter(is_default=True).exists():
            return not getattr(self.permissions.filter(is_default=True).first(), 'can_view', True)
        return False

    @property
    def no_records(self):
        """Return count of records associated with record, if any."""
        return self.children.count()


class Record(index.Indexed, dalmeUuid, dalmeOwned):
    """Stores information about records."""

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    parent = GenericForeignKey('parent_type', 'parent_id')
    parent_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    parent_id = models.CharField(max_length=36, db_index=True, null=True)  # noqa: DJ001
    attributes = GenericRelation('Attribute', related_query_name='record')
    pages = models.ManyToManyField('Page', db_index=True, through='Folio')
    tags = GenericRelation('Tag')
    comments = GenericRelation('Comment')
    collections = GenericRelation('CollectionMembership', related_query_name='record')
    permissions = GenericRelation('Permission', related_query_name='record')
    relationships_as_source = GenericRelation(
        'Relationship',
        content_type_field='source_content_type',
        object_id_field='source_object_id',
    )
    relationships_as_target = GenericRelation(
        'Relationship',
        content_type_field='target_content_type',
        object_id_field='target_object_id',
    )

    search_fields = [index.FilterField('name')]

    def __str__(self):  # noqa: D105
        return self.name

    def get_absolute_url(self):
        """Return absolute url for record."""
        return reverse('source_detail', kwargs={'pk': self.pk})

    @property
    def is_published(self):
        """Return boolean indicating whether the record has been published."""
        try:
            return self.workflow.is_public
        except Workflow.DoesNotExist:
            return False

    @property
    def comment_count(self):
        """Return count of comments."""
        return self.comments.count()

    @property
    def is_private(self):
        """Return boolean indicating whether the record is private."""
        if self.permissions.filter(is_default=True).exists():
            return not getattr(self.permissions.filter(is_default=True).first(), 'can_view', True)
        return False

    def get_related_resources(self, content_type):
        """Return list of resources of type:content_type associated with the record, if any."""
        res_list = []
        for page in self.folios.all().select_related('transcription'):
            if page.transcription:
                res_list.append(page.transcription.entity_phrases.filter(content_type=content_type))

        return list(res_list[0].union(*res_list[1:])) if len(res_list) > 0 else None

    def agents(self):
        """Return list of agents associated with the record, if any."""
        return self.get_related_resources(104)

    def places(self):
        """Return list of places associated with the record, if any."""
        return self.get_related_resources(115)

    def objects(self):
        """Return list of objects associated with the record, if any."""
        return self.get_related_resources(118)

    @property
    def has_images(self):
        """Return boolean indicating whether the record has associated images."""
        return self.pages.exclude(dam_id__isnull=True).exists()

    @property
    def no_images(self):
        """Return count of images associated with the record, if any."""
        return self.pages.exclude(dam_id__isnull=True).count() if self.has_images else 0

    @property
    def has_transcriptions(self):
        """Return boolean indicating whether the record has associated transcriptions."""
        return self.folios.all().select_related('transcription').exists()

    @property
    def no_transcriptions(self):
        """Return count of transcriptions associated with the record, if any."""
        return self.folios.exclude(transcription__count_ignore=True).count() if self.has_transcriptions else 0

    @property
    def no_folios(self):
        """Return count of folios associated with the record, if any."""
        return self.pages.all().count() if self.pages.all().exists() else 0

    def get_purl(self):
        """Return the record's permanent url."""
        return f'https://purl.dalme.org/{self.id}/' if self.workflow.is_public else None

    def get_credits(self):
        """Return credits for record as list of dicts."""
        return [
            {'name': r.source.name, 'credit': r.scopes.parameters.credit}
            for r in self.relationships_as_target.filter(
                rel_type__short_name='authorship',
                scopes__parameters__credit__in=['editor', 'corrections', 'contributor'],
            )
        ]

    def get_credit_line(self):
        """Return credit line for the record, if applicable."""

        def get_people_string(p_list):
            if len(p_list) == 1:
                return f'{p_list[0]}'
            if len(p_list) == 2:  # noqa: PLR2004
                return f'{p_list[0]} and {p_list[1]}'
            return f'{", ".join(p_list[:-1])}, and {p_list[-1]}'

        try:
            editors = [i.name for i in self.get_credits() if i.credit == 'editor']
            corrections = [i.name for i in self.get_credits() if i.credit == 'corrections']
            contributors = [i.name for i in self.get_credits() if i.credit == 'contributors']

            if not editors:
                try:
                    editors = [self.owner.agent.first().standard_name]
                except:  # noqa: E722
                    editors = ['the DALME Team']

            ed_str = get_people_string(editors)
            cor_str = get_people_string(corrections) if corrections else False
            cont_str = get_people_string(contributors) if contributors else False

            cline = f'Edited by {ed_str}'
            cline = cline + f', with corrections by {cor_str}' if corrections else cline
            cline = cline + f', and contributions by {cont_str}' if corrections and contributors else cline
            cline = cline + f', with contributions by {cont_str}' if contributors and not corrections else cline
            cline = cline + '.'

            return {'credit_line': cline, 'authors': editors, 'contributors': corrections + contributors}

        except:  # noqa: E722
            return {'credit_line': 'Edited by the DALME Team.', 'authors': ['The DALME Team'], 'contributors': []}


class Folio(dalmeIntid):
    """Links records, pages, and transcriptions."""

    record = models.ForeignKey(
        'Record',
        to_field='id',
        db_index=True,
        on_delete=models.CASCADE,
        related_name='folios',
    )
    page = models.ForeignKey(
        'Page',
        to_field='id',
        db_index=True,
        on_delete=models.CASCADE,
        related_name='records',
    )
    transcription = models.ForeignKey(
        'Transcription',
        to_field='id',
        db_index=True,
        on_delete=models.SET_NULL,
        null=True,
        related_name='folios',
    )

    @property
    def page_data(self):
        """Return a dictionary with aggregated folio/page information."""
        return {
            'id': self.page.id,
            'name': self.page.name,
            'dam_id': self.page.dam_id,
            'order': self.page.order,
            'transcription_id': self.transcription.id if self.transcription else None,
            'has_image': self.page is not None,
            'has_transcription': self.transcription is not None,
            'transcription_text': self.transcription.transcription if self.transcription is not None else None,
            'transcription_version': self.transcription.version if self.transcription is not None else None,
            'transcription_author': self.transcription.author if self.transcription is not None else None,
            'thumbnail_url': self.page.thumbnail_url,
            'manifest_url': self.page.manifest_url,
        }
