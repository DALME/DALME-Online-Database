import json
from contextlib import suppress

from rest_framework import serializers

from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin


class JWTUserDetailsSerializer(serializers.ModelSerializer):
    """User serializer for JWT tokens."""

    full_name = serializers.CharField(max_length=255, source='profile.full_name', required=False)
    avatar = serializers.CharField(max_length=255, source='profile.profile_image', required=False)
    is_admin = serializers.SerializerMethodField()
    preferences = serializers.JSONField(source='profile.preferences', required=False)

    class Meta:  # noqa: D106
        model = auth.models.User
        fields = ('id', 'username', 'full_name', 'email', 'avatar', 'is_admin', 'preferences')
        read_only_fields = ('email', 'is_admin')

    def get_is_admin(self, obj):
        """Return boolean indicating whether user is admin."""
        return any(group.name == "Administrators" for group in obj.groups.all())

    @staticmethod
    def validate_username(username):
        """Override method to prevent validation."""
        return username


class JWTSessionAuthentication(MiddlewareMixin):
    """Session authentication for JWT tokens."""

    def __init__(self, get_response):  # noqa: D107
        super().__init__(get_response)

    def process_request(self, request):
        """Process the request and add session login."""
        if request.path == '/api/jwt/login/':
            with suppress(Exception):
                payload = json.loads(request.body)
                username = payload.get('username')
                password = payload.get('password')
                if username and password:
                    user = auth.authenticate(request, username=username, password=password)
                    if user is not None and user.is_active:
                        auth.login(request, user)
                        self.create_session(request, user)

    def process_response(self, request, response):
        """Process the response and add session logout."""
        if request.path == '/api/jwt/logout/' and response.status_code == 200:  # noqa: PLR2004
            with suppress(Exception):
                auth.logout(request)

        return response

    @staticmethod
    def create_session(request, user):
        """Create the session (adapted from the Django login method)."""
        request.session.clear()
        request.session.cycle_key()
        request.session[auth.SESSION_KEY] = user._meta.pk.value_to_string(user)  # noqa: SLF001
        request.session[auth.BACKEND_SESSION_KEY] = 'django.contrib.auth.backends.ModelBackend'
        request.session[auth.HASH_SESSION_KEY] = user.get_session_auth_hash()
        request.session.save()
