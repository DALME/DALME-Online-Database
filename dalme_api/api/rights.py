"""API endpoint for managing rights."""
from dalme_api.access_policies import RightsAccessPolicy
from dalme_api.filters import RightsPolicyFilter
from dalme_api.serializers import RightsPolicySerializer
from dalme_app.models import RightsPolicy

from .base_viewset import DALMEBaseViewSet


class Rights(DALMEBaseViewSet):
    """API endpoint for managing rights policies."""

    permission_classes = (RightsAccessPolicy,)
    queryset = RightsPolicy.objects.all()
    serializer_class = RightsPolicySerializer
    filterset_class = RightsPolicyFilter
    search_fields = ['name', 'rights_holder', 'rights', 'licence']
    ordering = ['id']
    ordering_fields = [
        'id',
        'name',
        'rights_holder',
        'public_display',
        'creation_user',
        'creation_timestamp',
        'notice_display',
    ]
