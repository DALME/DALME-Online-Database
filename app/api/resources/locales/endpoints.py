"""API endpoint for managing locales."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from api.access_policies import BaseAccessPolicy
from api.base_viewset import IDABaseViewSet
from domain.models import LocaleReference

from .serializers import LocaleReferenceSerializer


class LocaleAccessPolicy(BaseAccessPolicy):
    """Access policies for Locales endpoint."""

    id = 'locales-policy'


class Locales(IDABaseViewSet):
    """API endpoint for managing locales."""

    permission_classes = [LocaleAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & LocaleAccessPolicy]

    queryset = LocaleReference.objects.all()
    serializer_class = LocaleReferenceSerializer
    filterset_fields = ['id', 'name', 'administrative_region', 'country__name']
    search_fields = ['id', 'name', 'administrative_region', 'country__name']
    ordering_fields = ['id', 'name', 'administrative_region', 'country', 'latitude', 'longitude']
    ordering = ['name']
