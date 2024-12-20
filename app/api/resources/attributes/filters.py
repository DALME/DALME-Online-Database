"""Define API filtering for attribute resources."""

from django_filters import rest_framework as filters

from domain.models import ContentTypeExtended


class ContentTypeFilter(filters.FilterSet):
    """Filter for ContentTypes endpoint."""

    id__lt = filters.NumberFilter(field_name='id', lookup_expr='lt')

    class Meta:
        model = ContentTypeExtended
        fields = ['id']
