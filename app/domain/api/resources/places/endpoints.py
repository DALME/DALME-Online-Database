"""API endpoint for managing places."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from app.access_policies import BaseAccessPolicy
from domain.api.viewsets import BaseViewSet
from domain.models import Place

from .serializers import PlaceSerializer


class PlaceAccessPolicy(BaseAccessPolicy):
    """Access policies for Places endpoint."""

    id = 'places-policy'


class Places(BaseViewSet):
    """API endpoint for managing places."""

    permission_classes = [PlaceAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & PlaceAccessPolicy]

    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    filterset_fields = ['id']
    search_fields = ['id', 'name']
    ordering_fields = ['id', 'name']
    ordering = ['name']
