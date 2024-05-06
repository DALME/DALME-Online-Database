"""Filters for team extension."""

import django_filters

from django.contrib import auth

from .models import TeamMember


class IdInFilter(django_filters.BaseInFilter, django_filters.NumberFilter):
    pass


class TeamMemberFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label='Name', lookup_expr='icontains')
    id__in = IdInFilter(field_name='id', lookup_expr='in')

    order_by = 'name'

    class Meta:
        model = TeamMember
        fields = [
            'id__in',
            'name',
            'roles',
        ]


class UserFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='wagtail_userprofile__profile__full_name', lookup_expr='icontains')
    id__in = IdInFilter(field_name='id', lookup_expr='in')

    order_by = 'name'

    class Meta:
        model = auth.get_user_model()
        fields = [
            'id',
            'id__in',
            'name',
        ]
