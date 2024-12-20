"""API endpoint for managing locations."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from api.access_policies import GeneralAccessPolicy
from api.base_viewset import IDABaseViewSet
from domain.models import Location

from .serializers import LocationSerializer


class Locations(IDABaseViewSet):
    """API endpoint for managing places."""

    permission_classes = [GeneralAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & GeneralAccessPolicy]

    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filterset_fields = ['id', 'location_type']
    search_fields = ['id', 'location_type']
    ordering_fields = ['id', 'location_type']
    ordering = ['id']
