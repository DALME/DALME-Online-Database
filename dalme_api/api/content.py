"""API endpoint for managing ContentTypes."""
from dalme_api.access_policies import GeneralAccessPolicy
from dalme_api.filters import ContentTypeFilter
from dalme_api.serializers import ContentTypeSerializer
from dalme_app.models import ContentTypeExtended

from .base_viewset import DALMEBaseViewSet


class ContentTypes(DALMEBaseViewSet):
    """API endpoint for managing ContentTypes."""

    permission_classes = (GeneralAccessPolicy,)
    queryset = ContentTypeExtended.objects.all()
    serializer_class = ContentTypeSerializer
    filterset_class = ContentTypeFilter
