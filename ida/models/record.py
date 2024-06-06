"""Record-related models."""

from wagtail.search import index

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Q, options
from django.utils.functional import cached_property

from ida.models.utils import (
    CommentMixin,
    HistoricalDateRange,
    OwnedMixin,
    PermissionsMixin,
    RelationshipMixin,
    ScopedBase,
    TaggingMixin,
    TrackingMixin,
    UuidMixin,
    format_credit_line,
    format_credits,
    format_source,
)
from ida.models.utils.attribute_mixin import AttributeMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db', 'attribute_matching_fields')


class RecordGroup(
    UuidMixin,
    TrackingMixin,
    OwnedMixin,
    AttributeMixin,
    CommentMixin,
    PermissionsMixin,
    TaggingMixin,
):
    """Stores information about archival units."""

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    parent = GenericForeignKey('parent_type', 'parent_id')
    parent_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    parent_id = models.CharField(max_length=36, db_index=True, null=True)
    children = GenericRelation('ida.Record', related_query_name='record_group')

    @cached_property
    def is_private(self):
        """Return boolean indicating whether the record is private."""
        if self.permissions.filter(is_default=True).exists():
            return not getattr(self.permissions.filter(is_default=True).first(), 'can_view', True)
        return False

    @cached_property
    def no_records(self):
        """Return count of records associated with record, if any."""
        return self.children.count()


class Record(
    index.Indexed,
    UuidMixin,
    TrackingMixin,
    OwnedMixin,
    AttributeMixin,
    CommentMixin,
    PermissionsMixin,
    RelationshipMixin,
    TaggingMixin,
):
    """Stores information about records."""

    name = models.CharField(max_length=255)
    short_name = models.CharField(max_length=55)
    parent = GenericForeignKey('parent_type', 'parent_id')
    parent_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    parent_id = models.CharField(max_length=36, db_index=True, null=True)
    pages = models.ManyToManyField('ida.Page', db_index=True, through='ida.PageNode')
    collections = GenericRelation('ida.CollectionMembership', related_query_name='record')

    search_fields = [index.FilterField('name')]

    class Meta:
        base_manager_name = 'objects'
        default_manager_name = 'objects'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """Return absolute url for record."""
        return f'{settings.BASE_URL}/api/records/{self.pk}/'

    @cached_property
    def is_published(self):
        """Return boolean indicating whether the record has been published."""
        try:
            return self.workflow.is_public
        except self._meta.get_field('workflow').related_model.DoesNotExist:
            return False

    def get_date(self):
        df = ['date', 'start_date', 'end_date']
        dates = {
            i['name']: i['value'] for i in self.attributes.filter(attribute_type__name__in=df).values('name', 'value')
        }
        if not any(dates.get(i) for i in df):
            return None
        if dates.get('date'):
            return dates['date']
        if dates.get('start_date') and dates.get('end_date'):
            return HistoricalDateRange(dates['start_date'], dates['end_date'])
        return next(dates.get(i) for i in df if i)

    @cached_property
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

    @cached_property
    def has_images(self):
        """Return boolean indicating whether the record has associated images."""
        return self.pages.exclude(dam_id__isnull=True).exists()

    @cached_property
    def no_images(self):
        """Return count of images associated with the record, if any."""
        return self.pages.exclude(dam_id__isnull=True).count() if self.has_images else 0

    @cached_property
    def has_transcriptions(self):
        """Return boolean indicating whether the record has associated transcriptions."""
        return self.pagenodes.all().select_related('transcription').exists()

    @cached_property
    def no_transcriptions(self):
        """Return count of transcriptions associated with the record, if any."""
        return len(
            [t for t in self.pagenodes.all() if t.transcription is not None and t.transcription.count_transcription]
        )

    @property
    def no_folios(self):
        """Return count of folios associated with the record, if any."""
        return self.pages.count() if self.pages.exists() else 0

    def get_purl(self):
        """Return the record's permanent url."""
        return f'{settings.BASE_URL}/purl/{self.id}/' if self.is_published else None

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
        return format_credits(self)

    def get_credit_line(self):
        """Return standard credit line for the record, if applicable."""
        return format_credit_line(self)

    def get_source(self):
        """Return source information for the record."""
        return format_source(self)

    def get_named_persons(self):
        """Return a list of persons named in the record."""
        # TODO: fix named_persons attribute
        return


class RecordType(ScopedBase, TrackingMixin):
    """Defines record types (tenanted)."""

    name = models.CharField(max_length=255)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        related_name='subtypes',
    )
    description = models.TextField(blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(name='unique_name_parent', fields=['name', 'parent'])]
        attribute_matching_fields = ['name', 'label']

    def __str__(self):
        return self.label

    @property
    def label(self):
        if self.parent:
            return f'{self.parent.name}-{self.name}'
        return self.name

    @property
    def group(self):
        if self.parent:
            return self.parent.name
        if self.subtypes.exists():
            return self.name
        return 'Other'


class PageNode(TrackingMixin):
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
