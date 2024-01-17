"""API endpoint for managing locales."""
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from dalme_api.access_policies import BaseAccessPolicy
from dalme_api.base_viewset import DALMEBaseViewSet
from ida.models import LocaleReference

from .serializers import LocaleReferenceSerializer


class LocaleAccessPolicy(BaseAccessPolicy):
    """Access policies for Locales endpoint."""

    id = 'locales-policy'  # noqa: A003


class Locales(DALMEBaseViewSet):
    """API endpoint for managing locales."""

    permission_classes = [LocaleAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope]

    queryset = LocaleReference.objects.all()
    serializer_class = LocaleReferenceSerializer
    filterset_fields = ['id', 'name', 'administrative_region', 'country__name']
    search_fields = ['id', 'name', 'administrative_region', 'country__name']
    ordering_fields = ['id', 'name', 'administrative_region', 'country', 'latitude', 'longitude']
    ordering = ['name']
