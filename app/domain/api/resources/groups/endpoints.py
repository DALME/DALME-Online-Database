"""API endpoint for managing user groups."""

from oauth2_provider.contrib.rest_framework import TokenHasScope

from django.contrib.auth.models import Group

from app.access_policies import GeneralAccessPolicy
from domain.api.viewsets import BaseViewSet

from .serializers import GroupSerializer


class Groups(BaseViewSet):
    """API endpoint for managing user groups."""

    serializer_class = GroupSerializer
    permission_classes = [GeneralAccessPolicy]
    oauth_permission_classes = [TokenHasScope]
    required_scopes = ['read', 'write', 'groups']
    queryset = Group.objects.all()

    filterset_fields = [
        'id',
        'name',
        'properties__group_type',
        'properties__tenant',
    ]
    search_fields = ['name']
    ordering_fields = ['id', 'name']
    ordering = ['name']

    # def get_queryset(self):
    #     """Make sure that groups are correctly filtered over tenants."""
    #     return self.request.user.groups_scoped
