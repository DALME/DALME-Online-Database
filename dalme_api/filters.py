from django_filters import rest_framework as filters

from django.contrib.auth.models import User

from dalme_app.models import Collection, ContentTypeExtended, Record, RightsPolicy, Task, Ticket


class ContentTypeFilter(filters.FilterSet):
    """Filter for ContentTypes endpoint."""

    id__lt = filters.NumberFilter(field_name='id', lookup_expr='lt')

    class Meta:  # noqa: D106
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

    class Meta:  # noqa: D106
        model = Record
        fields = [
            'name',
            'short_name',
            'owner',
        ]


class RightsPolicyFilter(filters.FilterSet):
    """Filter for Rights endpoint."""

    class Meta:  # noqa: D106
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

    class Meta:  # noqa: D106
        model = Collection
        fields = ['name', 'is_published']


class TaskFilter(filters.FilterSet):
    """Filter for Tasks endpoint."""

    class Meta:  # noqa: D106
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'completed',
            'url',
            'creation_user',
            'creation_timestamp',
        ]


class TicketFilter(filters.FilterSet):
    """Filter for Tickets endpoint."""

    # tags = filters.CharFilter(field_name='tags__tag', lookup_expr='icontains')

    class Meta:  # noqa: D106
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

    class Meta:  # noqa: D106
        model = User
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
