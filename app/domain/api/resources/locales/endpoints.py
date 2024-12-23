"""API endpoint for managing locales."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from app.access_policies import BaseAccessPolicy
from domain.api.viewsets import BaseViewSet
from domain.models import LocaleReference

from .serializers import LocaleReferenceSerializer


class LocaleAccessPolicy(BaseAccessPolicy):
    """Access policies for Locales endpoint."""

    id = 'locales-policy'


class Locales(BaseViewSet):
    """API endpoint for managing locales."""

    permission_classes = [LocaleAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & LocaleAccessPolicy]

    queryset = LocaleReference.objects.all()
    serializer_class = LocaleReferenceSerializer
    filterset_fields = ['id', 'name', 'administrative_region', 'country__name']
    search_fields = ['id', 'name', 'administrative_region', 'country__name']
    ordering_fields = ['id', 'name', 'administrative_region', 'country', 'latitude', 'longitude']
    ordering = ['name']
