"""API endpoint for managing places."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from api.access_policies import BaseAccessPolicy
from api.base_viewset import IDABaseViewSet
from ida.models import Place

from .serializers import PlaceSerializer


class PlaceAccessPolicy(BaseAccessPolicy):
    """Access policies for Places endpoint."""

    id = 'places-policy'


class Places(IDABaseViewSet):
    """API endpoint for managing places."""

    permission_classes = [PlaceAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope]

    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filterset_fields = ['id']
    search_fields = ['id', 'name']
    ordering_fields = ['id', 'name']
    ordering = ['name']
