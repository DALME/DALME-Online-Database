"""API endpoint for managing locations."""
from dalme_api.access_policies import GeneralAccessPolicy
from dalme_api.serializers import LocationSerializer
from dalme_app.models import Location

from .base_viewset import DALMEBaseViewSet


class Locations(DALMEBaseViewSet):
    """API endpoint for managing places."""

    permission_classes = (GeneralAccessPolicy,)
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filterset_fields = ['id', 'location_type']
    search_fields = ['id', 'location_type']
    ordering_fields = ['id', 'location_type']
    ordering = ['id']
