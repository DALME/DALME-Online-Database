"""API endpoint for managing users."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from app.access_policies import BaseAccessPolicy
from domain.api.viewsets import BaseViewSet

from .filters import UserFilter
from .serializers import UserSerializer


class UserAccessPolicy(BaseAccessPolicy):
    """Access policies for Users endpoint."""

    id = 'users-policy'


class Users(BaseViewSet):
    """API endpoint for managing users."""

    permission_classes = [UserAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & UserAccessPolicy]

    lookup_url_kwarg = 'pk'
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter
    search_fields = ['username', 'email', 'full_name', 'first_name', 'last_name']
    ordering_fields = [
        'id',
        'username',
        'email',
        'full_name',
        'last_login',
        'date_joined',
        'is_staff',
        'is_active',
        'is_superuser',
        'first_name',
    ]
    ordering = ['-is_active', 'username']

    def get_object(self):
        """Return the object the view is displaying by id or username."""
        lookup = self.kwargs.get(self.lookup_url_kwarg)
        if lookup is not None and not lookup.isdigit():
            self.lookup_field = 'username'
        return super().get_object()

    def update(self, request, *args, **kwargs):  # noqa: ARG002
        """Update user record."""
        partial = True
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial,
            fields=[
                'id',
                'is_superuser',
                'username',
                'first_name',
                'last_name',
                'email',
                'is_staff',
                'is_active',
                'groups',
                'profile',
            ],
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data, 200)
