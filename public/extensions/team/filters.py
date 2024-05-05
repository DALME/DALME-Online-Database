"""Filters for team extension."""

import django_filters

from .models import TeamMember


class TeamMemberFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label='Name', lookup_expr='icontains')

    order_by = 'name'

    class Meta:
        model = TeamMember
        fields = [
            'name',
            'roles',
        ]
