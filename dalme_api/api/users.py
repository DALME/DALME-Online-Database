"""API endpoint for managing users."""
import json
import pathlib

from rest_framework.decorators import action
from rest_framework.response import Response

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpRequest

from dalme_api.access_policies import UserAccessPolicy
from dalme_api.filters import UserFilter
from dalme_api.serializers import UserSerializer

from .base_viewset import DALMEBaseViewSet

with pathlib.Path('static/snippets/default_user_preferences.json').open() as fp:
    DEFAULT_PREFS = json.load(fp)


class Users(DALMEBaseViewSet):
    """API endpoint for managing users."""

    lookup_url_kwarg = 'pk'
    permission_classes = (UserAccessPolicy,)
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    filterset_class = UserFilter
    search_fields = ['username', 'email', 'profile__full_name', 'first_name', 'last_name']
    ordering_fields = [
        'id',
        'username',
        'email',
        'profile__full_name',
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

    @action(detail=True, methods=['post'])
    def reset_password(self, request, *args, **kwargs):  # noqa: ARG002
        """Reset user password."""
        obj = self.get_object()
        try:
            form = PasswordResetForm({'email': obj.email})
            assert form.is_valid()
            request = HttpRequest()
            request.META['SERVER_NAME'] = 'db.dalme.org'
            request.META['SERVER_PORT'] = '443'
            form.save(
                request=request,
                use_https=settings.USE_HTTPS,
                from_email=settings.DEFAULT_FROM_EMAIL,
                email_template_name='registration/password_reset_email.html',
            )
            return Response({'data': 'Email sent'}, 201)

        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)

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
        try:
            if not user.profile.preferences:
                user.profile.preferences = DEFAULT_PREFS
            return Response(user.profile.preferences, 201)

        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)

    @action(detail=True, methods=['post'])
    def update_preferences(self, request, *args, **kwargs):  # noqa: ARG002
        """Update user preferences."""
        user = self.get_object()
        try:
            if request.data:
                prefs = user.profile.preferences if user.profile.preferences else DEFAULT_PREFS
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
