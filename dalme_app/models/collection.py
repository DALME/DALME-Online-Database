"""Model collection data."""
from collections import Counter

from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import options

from dalme_app.models.templates import dalmeBasic, dalmeOwned, dalmeUuid

from .scoped import ScopedBase

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Collection(ScopedBase, dalmeUuid, dalmeOwned):
    """Stores collection information."""

    name = models.CharField(max_length=255)
    use_as_workset = models.BooleanField(default=False)
    is_published = models.BooleanField(default=False)
    team_link = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name='default_collection',
        limit_choices_to={'properties__type': 3},
        null=True,
    )
    attributes = GenericRelation('Attribute', related_query_name='collection')
    permissions = GenericRelation('Permission', related_query_name='collection')
    comments = GenericRelation('Comment')

    def __str__(self):
        return self.name

    @property
    def comment_count(self):
        """Return count of comments."""
        return self.comments.count()

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
            query = models.Q(record__attributes__attribute_type=15)

            if published:
                query.add(models.Q(record__workflow__is_public=True), models.Q.AND)

            return list(
                self.members.filter(query)
                .distinct()
                .order_by('record__attributes__attributevaluefkey__language__name')
                .values_list(
                    'record__attributes__attributevaluefkey__language__name',
                    'record__attributes__attributevaluefkey__language__id',
                ),
            )

        return None

    def get_time_coverage(self, published=False):
        """Return a list of years and counts represented in the collection (if all members are records)."""
        if self.membership_type() == 'record':
            query = models.Q(record__attributes__attribute_type__in=[19, 25, 26])

            if published:
                query.add(models.Q(record__workflow__is_public=True), models.Q.AND)

            years = (
                self.members.filter(query)
                .order_by('record__attributes__attributevaluedate__year')
                .values_list('record__attributes__attributevaluedate__year', flat=True)
            )

            return dict(Counter(years))
        return None


class CollectionMembership(ScopedBase, dalmeBasic):
    """Links collections and members."""

    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='members')
    content_object = GenericForeignKey('content_type', 'object_id')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.CharField(max_length=36, db_index=True)

    class Meta:
        unique_together = ('content_type', 'object_id', 'collection')
        ordering = ['collection', 'id']
