"""API endpoint for managing countries."""
from dalme_api.access_policies import GeneralAccessPolicy
from dalme_api.serializers import CountryReferenceSerializer
from dalme_app.models import CountryReference

from .base_viewset import DALMEBaseViewSet


class Countries(DALMEBaseViewSet):
    """API endpoint for managing countries."""

    permission_classes = (GeneralAccessPolicy,)
    queryset = CountryReference.objects.all()
    serializer_class = CountryReferenceSerializer
    filterset_fields = ['id', 'name', 'alpha_3_code', 'alpha_2_code', 'num_code']
    search_fields = ['id', 'name', 'alpha_3_code', 'alpha_2_code', 'num_code']
    ordering_fields = ['id', 'name', 'alpha_3_code', 'alpha_2_code', 'num_code']
    ordering = ['name']
