"""API endpoint for managing languages."""
from dalme_api.access_policies import GeneralAccessPolicy
from dalme_api.serializers import LanguageReferenceSerializer
from dalme_app.models import LanguageReference

from .base_viewset import DALMEBaseViewSet


class Languages(DALMEBaseViewSet):
    """API endpoint for managing languages."""

    permission_classes = (GeneralAccessPolicy,)
    queryset = LanguageReference.objects.all()
    serializer_class = LanguageReferenceSerializer
    filterset_fields = ['id', 'name', 'is_dialect', 'parent__name', 'iso6393', 'glottocode']
    search_fields = ['id', 'name', 'is_dialect', 'parent__name', 'iso6393', 'glottocode']
    ordering_fields = ['id', 'name', 'is_dialect', 'parent', 'iso6393', 'glottocode']
    ordering = ['name']
