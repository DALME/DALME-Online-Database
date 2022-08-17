import json
from django.conf import settings
from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token


class JWTUserDetailsSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(max_length=255, source='profile.full_name', required=False)
    avatar = serializers.CharField(max_length=255, source='profile.profile_image', required=False)
    isAdmin = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'full_name', 'email', 'avatar', 'isAdmin')
        read_only_fields = ('email', 'isAdmin')

    def get_isAdmin(self, obj):
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
                user = authenticate(
                    request,
                    username=payload['username'],
                    password=payload['password']
                )
                login(request, user)
            except:  # NOQA
                pass

    def process_response(self, request, response):
        if request.path == '/api/jwt/logout/' and response.status_code == 200:
            try:
                logout(request)
            except:  # NOQA
                pass

        return response
