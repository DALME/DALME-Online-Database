"""API endpoint for managing user groups."""
from oauth2_provider.contrib.rest_framework import TokenHasScope

from dalme_api.access_policies import GeneralAccessPolicy
from dalme_api.base_viewset import DALMEBaseViewSet

from .serializers import GroupSerializer


class Groups(DALMEBaseViewSet):
    """API endpoint for managing user groups."""

    serializer_class = GroupSerializer

    permission_classes = [GeneralAccessPolicy]
    oauth_permission_classes = [TokenHasScope]
    required_scopes = ['read', 'write', 'groups']

    filterset_fields = [
        'id',
        'name',
        'properties__group_type',
        'properties__tenant',
    ]
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    ordering = ['name']

    def get_queryset(self):
        """Make sure that groups are correctly filtered over tenants."""
        return self.request.user.groups_scoped
