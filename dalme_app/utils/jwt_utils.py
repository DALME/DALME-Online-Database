import json
from django.contrib import auth
from rest_framework import serializers
from django.utils.deprecation import MiddlewareMixin


class JWTUserDetailsSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=255, source='profile.full_name', required=False)
    avatar = serializers.CharField(max_length=255, source='profile.profile_image', required=False)
    is_admin = serializers.SerializerMethodField()

    class Meta:
        model = auth.models.User
        fields = ('id', 'username', 'full_name', 'email', 'avatar', 'is_admin')
        read_only_fields = ('email', 'is_admin')

    def get_is_admin(self, obj):
        return any(
            group.name == "Administrators"
            for group in obj.groups.all()
        )

    @staticmethod
    def validate_username(username):
        return username


class JWTSessionAuthentication(MiddlewareMixin):

    def __init__(self, get_response):
        super().__init__(get_response)

    def process_request(self, request):
        if request.path == '/api/jwt/login/':
            try:
                payload = json.loads(request.body)
                username = payload.get('username')
                password = payload.get('password')
                if username and password:
                    user = auth.authenticate(request, username=username, password=password)
                    if user is not None and user.is_active:
                        auth.login(request, user)
                        self.create_session(request, user)
            except:  # NOQA
                pass

    def process_response(self, request, response):
        if request.path == '/api/jwt/logout/' and response.status_code == 200:
            try:
                auth.logout(request)
            except:  # NOQA
                pass

        return response

    @staticmethod
    def create_session(request, user):
        """Adapted from the Django login method.
        https://github.com/django/django/blob/7cca22964c09e8dafc313a400c428242404d527a/django/contrib/auth/__init__.py#L90
        """
        request.session.clear()
        request.session.cycle_key()
        request.session[auth.SESSION_KEY] = user._meta.pk.value_to_string(user)
        request.session[auth.BACKEND_SESSION_KEY] = 'django.contrib.auth.backends.ModelBackend'
        request.session[auth.HASH_SESSION_KEY] = user.get_session_auth_hash()
        request.session.save()
