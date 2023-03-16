"""API endpoint for managing places."""
from dalme_api.access_policies import PlaceAccessPolicy
from dalme_api.serializers import PlaceSerializer
from dalme_app.models import Place

from .base_viewset import DALMEBaseViewSet


class Places(DALMEBaseViewSet):
    """API endpoint for managing places."""

    permission_classes = (PlaceAccessPolicy,)
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filterset_fields = ['id']
    search_fields = ['id', 'name']
    ordering_fields = ['id', 'name']
    ordering = ['name']
