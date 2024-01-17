"""API endpoint for managing countries."""
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from dalme_api.access_policies import GeneralAccessPolicy
from dalme_api.base_viewset import DALMEBaseViewSet
from ida.models import CountryReference

from .serializers import CountryReferenceSerializer


class Countries(DALMEBaseViewSet):
    """API endpoint for managing countries."""

    permission_classes = [GeneralAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope]

    queryset = CountryReference.objects.all()
    serializer_class = CountryReferenceSerializer
    filterset_fields = ['id', 'name', 'alpha_3_code', 'alpha_2_code', 'num_code']
    search_fields = ['id', 'name', 'alpha_3_code', 'alpha_2_code', 'num_code']
    ordering_fields = ['id', 'name', 'alpha_3_code', 'alpha_2_code', 'num_code']
    ordering = ['name']
