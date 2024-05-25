"""Record-related models."""

from wagtail.search import index

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q, options

from ida.models.templates import IntIdMixin, OwnedMixin, TrackedMixin, UuidMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class RecordGroup(UuidMixin, TrackedMixin, OwnedMixin):
    """Stores information about archival units."""

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    parent = GenericForeignKey('parent_type', 'parent_id')
    parent_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    parent_id = models.CharField(max_length=36, db_index=True, null=True)
    attributes = GenericRelation('ida.Attribute', related_query_name='record_group')
    children = GenericRelation('ida.Record', related_query_name='record_group')
    permissions = GenericRelation('ida.Permission', related_query_name='record_group')
    tags = GenericRelation('ida.Tag')
    comments = GenericRelation('ida.Comment')

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


class Record(index.Indexed, UuidMixin, TrackedMixin, OwnedMixin):
    """Stores information about records."""

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    parent = GenericForeignKey('parent_type', 'parent_id')
    parent_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    parent_id = models.CharField(max_length=36, db_index=True, null=True)
    attributes = GenericRelation('ida.Attribute', related_query_name='record')
    pages = models.ManyToManyField('ida.Page', db_index=True, through='ida.PageNode')
    tags = GenericRelation('ida.Tag')
    comments = GenericRelation('ida.Comment')
    collections = GenericRelation('ida.CollectionMembership', related_query_name='record')
    permissions = GenericRelation('ida.Permission', related_query_name='record')
    relationships_as_source = GenericRelation(
        'ida.Relationship',
        content_type_field='source_content_type',
        object_id_field='source_object_id',
    )
    relationships_as_target = GenericRelation(
        'ida.Relationship',
        content_type_field='target_content_type',
        object_id_field='target_object_id',
    )

    search_fields = [index.FilterField('name')]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Return absolute url for record."""
        return f'{settings.BASE_URL}/api/records/{self.pk}/'

    @property
    def is_published(self):
        """Return boolean indicating whether the record has been published."""
        try:
            return self.workflow.is_public
        except self._meta.get_field('workflow').related_model.DoesNotExist:
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
        for page in self.pagenodes.all().select_related('transcription'):
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
        return self.pagenodes.all().select_related('transcription').exists()

    @property
    def no_transcriptions(self):
        """Return count of transcriptions associated with the record, if any."""
        return len(
            [t for t in self.pagenodes.all() if t.transcription is not None and t.transcription.count_transcription]
        )

    @property
    def no_folios(self):
        """Return count of folios associated with the record, if any."""
        return self.pages.all().count() if self.pages.all().exists() else 0

    def get_purl(self):
        """Return the record's permanent url."""
        return f'{settings.BASE_URL}/purl/{self.id}/' if self.workflow.is_public else None

    def get_credit_data(self):
        """Return credit data for record as list of dicts."""
        return [
            {'name': r.source.name, 'credit': r.scopes.first().parameters['credit']}
            for r in self.relationships_as_target.filter(
                Q(rel_type__short_name='authorship')
                & (
                    Q(scopes__parameters__credit='editor')
                    | Q(scopes__parameters__credit='contributor')
                    | Q(scopes__parameters__credit='corrections')
                )
            )
        ]

    def get_credits(self):
        """Return credits for the record, if applicable."""
        try:
            c_data = self.get_credit_data()
            editors = [i['name'] for i in c_data if i['credit'] == 'editor']
            corrections = [i['name'] for i in c_data if i['credit'] == 'corrections']
            contributors = [i['name'] for i in c_data if i['credit'] == 'contributor']
        except:  # noqa: E722
            editors, corrections, contributors = [], [], []

        if not editors:
            try:  # noqa: SIM105
                editors = [self.owner.agent.first().standard_name]
            except:  # noqa: E722
                pass
        return (editors, corrections, contributors)


class PageNode(IntIdMixin, TrackedMixin):
    """Links records, pages, and transcriptions."""

    record = models.ForeignKey(
        'ida.Record',
        to_field='id',
        db_index=True,
        on_delete=models.CASCADE,
        related_name='pagenodes',
    )
    page = models.ForeignKey(
        'ida.Page',
        to_field='id',
        db_index=True,
        on_delete=models.CASCADE,
        related_name='records',
    )
    transcription = models.ForeignKey(
        'ida.Transcription',
        to_field='id',
        db_index=True,
        on_delete=models.SET_NULL,
        null=True,
        related_name='pagenodes',
    )
