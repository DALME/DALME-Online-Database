"""API endpoint for managing rights."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

from api.access_policies import BaseAccessPolicy
from api.base_viewset import IDABaseViewSet
from ida.models import RightsPolicy

from .filters import RightsPolicyFilter
from .serializers import RightsPolicySerializer


class RightsAccessPolicy(BaseAccessPolicy):
    """Access policies for Rights endpoint."""

    id = 'rights-policy'


class Rights(IDABaseViewSet):
    """API endpoint for managing rights policies."""

    permission_classes = [RightsAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope]

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
