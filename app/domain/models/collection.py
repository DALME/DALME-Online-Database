"""Collections-related models."""

from collections import Counter

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import options

from domain.models.abstract import OwnedMixin, TrackingMixin, UuidMixin
from domain.models.attribute import AttributeMixin
from domain.models.comment import CommentMixin
from domain.models.permission import PermissionMixin
from domain.models.tenant import TenantMixin

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Collection(
    TenantMixin,
    UuidMixin,
    TrackingMixin,
    OwnedMixin,
    AttributeMixin,
    CommentMixin,
    PermissionMixin,
):
    """Stores collection information."""

    name = models.CharField(max_length=255)
    use_as_workset = models.BooleanField(default=False)
    is_corpus = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    team_link = models.ForeignKey(
        'auth.Group',
        on_delete=models.CASCADE,
        related_name='default_collection',
        limit_choices_to={'properties__type': 3},
        null=True,
    )

    def __str__(self):
        return self.name

    @property
    def is_private(self):
        """Return boolean indicating whether the collection is private."""
        if self.permissions.filter(is_default=True).exists():
            return not getattr(self.permissions.filter(is_default=True).first(), 'can_view', True)
        return False

    def membership_type(self):
        """Return the type of members of the collection."""
        types = list({m.content_type.model for m in self.members.all()})
        return types[0] if len(types) == 1 else None if len(types) == 0 else types

    def member_count(self, published=False):
        """Return the count of members in the collection."""
        if published and self.membership_type() == 'record':
            return self.members.filter(record__workflow__is_public=True).count()
        return self.members.all().count()

    def get_languages(self, published=False):
        """Return a list of languages represented in the collection (if all members are records)."""
        if self.membership_type() == 'record':
            query = models.Q(record__attributes__attribute_type__name='language')

            if published:
                query.add(models.Q(record__workflow__is_public=True), models.Q.AND)

            return sorted(
                [
                    (i.name, i.id)
                    for i in self.members.filter(query)
                    .distinct()
                    .order_by('record__attributes__value__name')
                    .values_list('record__attributes__value', flat=True)
                ],
                key=lambda x: x[0],
            )

        return None

    def get_time_coverage(self, published=False):
        """Return a list of years and counts represented in the collection (if all members are records)."""
        if self.membership_type() == 'record':
            query = models.Q(record__attributes__attribute_type__name__in=['date', 'end_date', 'start_date'])

            if published:
                query.add(models.Q(record__workflow__is_public=True), models.Q.AND)

            years = sorted(
                [i.year for i in self.members.filter(query).values_list('record__attributes__value', flat=True)]
            )

            return dict(Counter(years))
        return None


class CollectionMembershipManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.annotate(
            col_id=models.F('collection__id'),
            col_name=models.F('collection__name'),
        )


class CollectionMembership(TenantMixin, TrackingMixin):
    """Links collections and members."""

    collection = models.ForeignKey('domain.Collection', on_delete=models.CASCADE, related_name='members')
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.CharField(max_length=36, db_index=True)
    order = models.IntegerField(null=True)

    objects = CollectionMembershipManager()

    class Meta:
        unique_together = ('content_type', 'object_id', 'collection')
        ordering = ['order', 'collection', 'id']
