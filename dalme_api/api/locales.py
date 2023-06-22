from dalme_api.access_policies import LocaleAccessPolicy
from dalme_api.serializers import LocaleReferenceSerializer
from dalme_app.models import LocaleReference

from .base_viewset import DALMEBaseViewSet


class Locales(DALMEBaseViewSet):
    """API endpoint for managing locales."""

    permission_classes = (LocaleAccessPolicy,)
    queryset = LocaleReference.objects.all()
    serializer_class = LocaleReferenceSerializer
    filterset_fields = ['id', 'name', 'administrative_region', 'country__name']
    search_fields = ['id', 'name', 'administrative_region', 'country__name']
    ordering_fields = ['id', 'name', 'administrative_region', 'country', 'latitude', 'longitude']
    ordering = ['name']
