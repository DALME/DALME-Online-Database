"""API endpoint for managing users."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.decorators import action
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from api.access_policies import BaseAccessPolicy
from api.base_viewset import IDABaseViewSet

from .filters import UserFilter
from .serializers import UserSerializer


class UserAccessPolicy(BaseAccessPolicy):
    """Access policies for Users endpoint."""

    id = 'users-policy'


class Users(IDABaseViewSet):
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
        return Response(serializer.data, 201)

    @action(detail=True, methods=['get'])
    def get_preferences(self, request, *args, **kwargs):  # noqa: ARG002
        """Return user preferences."""
        user = self.get_object()
        return Response(user.profile.preferences, 201)

    @action(detail=True, methods=['post'])
    def update_preferences(self, request, *args, **kwargs):  # noqa: ARG002
        """Update user preferences."""
        user = self.get_object()
        try:
            if request.data:
                prefs = user.profile.preferences
                if prefs.get(request.data['section']) is None:
                    prefs[request.data['section']] = {request.data['key']: request.data['value']}
                else:
                    prefs[request.data['section']][request.data['key']] = request.data['value']

                user.profile.preferences = prefs
                user.profile.save()

                return Response(201)

            return Response({'error': 'Request contained no data.'}, 400)

        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)
