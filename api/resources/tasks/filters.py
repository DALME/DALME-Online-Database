"""Define API filtering for task resources."""

from django_filters import rest_framework as filters

from django.contrib.auth import get_user_model
from django.db.models import Q

from ida.models import Task, TaskList


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
