"""API endpoint for managing rights."""
from dalme_api.access_policies import BaseAccessPolicy
from dalme_api.base_viewset import DALMEBaseViewSet
from dalme_api.filters import RightsPolicyFilter
from ida.models import RightsPolicy

from .serializers import RightsPolicySerializer


class RightsAccessPolicy(BaseAccessPolicy):
    """Access policies for Rights endpoint."""

    id = 'rights-policy'  # noqa: A003


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
