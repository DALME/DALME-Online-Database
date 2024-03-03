"""API endpoint for managing user groups."""

from oauth2_provider.contrib.rest_framework import TokenHasScope

from api.access_policies import GeneralAccessPolicy
from api.base_viewset import IDABaseViewSet

from .serializers import GroupSerializer


class Groups(IDABaseViewSet):
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
