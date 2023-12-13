"""Define API filtering logic and utilities."""
from django_filters import rest_framework as filters

from django.contrib.auth import get_user_model
from django.db.models import Q

from dalme_app.models import Collection, ContentTypeExtended, Record, Task, TaskList
from ida.models import RightsPolicy, Ticket


class ContentTypeFilter(filters.FilterSet):
    """Filter for ContentTypes endpoint."""

    id__lt = filters.NumberFilter(field_name='id', lookup_expr='lt')

    class Meta:
        model = ContentTypeExtended
        fields = ['id']


class RecordFilter(filters.FilterSet):
    """Filter for Records endpoint."""

    wf_status = filters.NumberFilter(field_name='workflow__wf_status', lookup_expr='iexact')
    wf_stage = filters.NumberFilter(field_name='workflow__stage', lookup_expr='iexact')
    help_flag = filters.BooleanFilter(field_name='workflow__help_flag')
    is_public = filters.BooleanFilter(field_name='workflow__is_public')
    ingestion_done = filters.BooleanFilter(field_name='workflow__ingestion_done')
    transcription_done = filters.BooleanFilter(field_name='workflow__transcription_done')
    markup_done = filters.BooleanFilter(field_name='workflow__markup_done')
    review_done = filters.BooleanFilter(field_name='workflow__review_done')
    parsing_done = filters.BooleanFilter(field_name='workflow__parsing_done')

    class Meta:
        model = Record
        fields = [
            'name',
            'short_name',
            'owner',
        ]


class RightsPolicyFilter(filters.FilterSet):
    """Filter for Rights endpoint."""

    class Meta:
        model = RightsPolicy
        fields = [
            'id',
            'name',
            'rights_holder',
            'rights_status',
            'rights',
            'public_display',
            'notice_display',
            'licence',
            'creation_timestamp',
            'creation_user',
            'modification_user',
            'modification_timestamp',
        ]


class CollectionFilter(filters.FilterSet):
    """Filter for Collections endpoint."""

    class Meta:
        model = Collection
        fields = ['name', 'is_published']


class TaskFilter(filters.FilterSet):
    """Filter for Tasks endpoint."""

    user = filters.CharFilter(label='user', method='for_user')

    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'completed',
            'completed_by',
            'url',
            'assignees',
            'creation_user',
            'creation_timestamp',
            'user',
        ]

    def for_user(self, queryset, name, value):  # noqa: ARG002
        """Return tasks the user in the request created, was assigned to, or completed."""
        return queryset.filter(
            Q(creation_user=value) | Q(completed_by=value) | Q(assignees=value),
        ).distinct()


class TasklistFilter(filters.FilterSet):
    """Filter for Tasklists endpoint."""

    user = filters.CharFilter(label='user', method='for_user')

    class Meta:
        model = TaskList
        fields = [
            'id',
            'name',
            'description',
            'slug',
            'creation_user',
            'creation_timestamp',
            'user',
        ]

    def for_user(self, queryset, name, value):  # noqa: ARG002
        """Return lists the user in the request owns, can see, or are linked to their teams/groups."""
        groups = [g.id for g in get_user_model().objects.get(pk=value).groups.all()]
        return queryset.filter(
            Q(owner=value)
            | Q(team_link__in=groups)
            | (Q(permissions__principal_id=value) & Q(permissions__can_view=True)),
        ).distinct()


class TicketFilter(filters.FilterSet):
    """Filter for Tickets endpoint."""

    # tags = filters.CharFilter(field_name='tags__tag', lookup_expr='icontains')

    class Meta:
        model = Ticket
        fields = [
            'id',
            'subject',
            'description',
            'status',
            'url',
            'creation_user',
            'creation_timestamp',
            'assigned_to',
        ]


class UserFilter(filters.FilterSet):
    """Filter for Users endpoint."""

    groups = filters.CharFilter(label='groups', method='check_groups')

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'profile__full_name',
            'groups',
        ]

    def check_groups(self, queryset, name, value):  # noqa: ARG002
        """Return combined group queryset."""
        request_groups = value.split(',') if ',' in value else [value]
        qs = queryset.none()
        for group in request_groups:
            qs = qs | queryset.filter(groups__name=group)

        return qs.distinct()
