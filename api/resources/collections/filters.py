"""Define API filtering for collection resources."""

from django_filters import rest_framework as filters

from ida.models import Collection


class CollectionFilter(filters.FilterSet):
    """Filter for Collections endpoint."""

    class Meta:
        model = Collection
        fields = ['name', 'is_published']
