"""Define API filtering for user resources."""

from django_filters import rest_framework as filters

from django.contrib.auth import get_user_model


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
