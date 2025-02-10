"""Define API filtering for rights resources."""

from django_filters import rest_framework as filters

from domain.models import RightsPolicy


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
