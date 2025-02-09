"""API endpoint for managing languages."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from app.access_policies import BaseAccessPolicy
from domain.api.viewsets import BaseViewSet
from domain.models import LanguageReference

from .serializers import LanguageReferenceSerializer


class LanguageAccessPolicy(BaseAccessPolicy):
    """Access policies for the Languages endpoint."""

    id = 'languages-policy'


class Languages(BaseViewSet):
    """API endpoint for managing languages."""

    permission_classes = [LanguageAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & LanguageAccessPolicy]

    queryset = LanguageReference.objects.all()
    serializer_class = LanguageReferenceSerializer
    filterset_fields = ['id', 'name', 'is_dialect', 'parent__name', 'iso6393', 'glottocode']
    search_fields = ['id', 'name', 'is_dialect', 'parent__name', 'iso6393', 'glottocode']
    ordering_fields = ['id', 'name', 'is_dialect', 'parent', 'iso6393', 'glottocode']
    ordering = ['name']
