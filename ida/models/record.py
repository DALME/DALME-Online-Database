"""Record-related models."""

from wagtail.search import index

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Case, Exists, ExpressionWrapper, Manager, OuterRef, Q, Subquery, When, options
from django.utils.functional import cached_property

from ida.models.attribute import Attribute
from ida.models.utils import (
    AttributeField,
    AttributeMixin,
    CommentMixin,
    OwnedMixin,
    PermissionsMixin,
    RelationshipMixin,
    ScopedBase,
    TaggingMixin,
    TrackingMixin,
    UuidMixin,
)

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


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


class RecordManager(Manager):
    def include_attrs(self, *args):
        qs = self.get_queryset()
        for attr in args:
            attr_sq = Attribute.objects.filter(ida_record_related=OuterRef('pk'), attribute_type__name=attr)
            qs = qs.annotate(
                **{
                    attr: ExpressionWrapper(
                        Case(When(Exists(attr_sq), then=Subquery(attr_sq.values_list('value', flat=True)[:1]))),
                        output_field=AttributeField(),
                    )
                }
            )
        return qs


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

    objects = RecordManager()

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

    # @cached_property
    # def date(self):
    #     dates = self.attributes.filter(name__in=['date', 'start_date', 'end_date'])
    #     return dates.first().value if dates.exists() else None

    # @cached_property
    # def record_type(self):
    #     rt = self.attributes.filter(name='record_type')
    #     return rt.first().value if rt.exists() else 'unclear'

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

    @cached_property
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
