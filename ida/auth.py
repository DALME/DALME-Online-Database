"""API endpoints for managing authentication and authorization."""
import json

from oauth2_provider.oauth2_validators import OAuth2Validator
from oauth2_provider.views import TokenView
from rest_framework import permissions, serializers, status, views
from rest_framework.response import Response

from django.conf import settings
from django.contrib.auth import authenticate, login

from dalme_api.access_policies import BaseAccessPolicy

from .tenant import get_current_tenant


class AuthAccessPolicy(BaseAccessPolicy):
    """Access policies for authorization and authentication."""

    id = 'auth-policy'  # noqa: A003


class LoginSerializer(serializers.Serializer):
    """Serializer for session login."""

    username = serializers.CharField(label='username', write_only=True)
    password = serializers.CharField(
        label='password', style={'input_type': 'password'}, trim_whitespace=True, write_only=True
    )

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)
            if not user:
                msg = 'Access denied: incorrect username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required fields.'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class AuthorizationCode(views.APIView):
    """API endpoint that receives the OIDC authorization token."""

    def get(self, request):  # noqa: ARG002
        return Response(None, status=status.HTTP_200_OK)


class Login(views.APIView):
    """API endpoint for session authentication login."""

    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):  # noqa: A002, ARG002
        serializer = LoginSerializer(data=self.request.data, context={'request': self.request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        login(request, user)

        return Response(None, status=status.HTTP_202_ACCEPTED)


class IDAOAuth2Validator(OAuth2Validator):
    """Override the built-in OAuth claims response."""

    def get_userinfo_claims(self, request):
        """Enhance the default OIDC claims payload."""
        claims = super().get_userinfo_claims(request)
        full_name = request.user.profile.full_name
        profile_image = request.user.profile.profile_image
        tenant = get_current_tenant()

        claims.update(
            {
                'avatar': profile_image,
                'email': request.user.email,
                'username': request.user.username,
                'full_name': full_name,
                'is_admin': request.user.is_staff,
                # TODO: groups: when multitenanted correctly...
                'tenant': {
                    'id': tenant.pk,
                    'name': tenant.name,
                },
            }
        )

        return claims


class OAuthToken(TokenView):
    """Override the django-oauth-toolkit token view.

    This allows us to return the refresh token in a HTTP only cookie instead of
    the response body, making things more secure against potential
    vulenerabilities.

    """

    permission_classes = [AuthAccessPolicy]

    def post(self, request, *args, **kwargs):
        """Generate the OAuth token response payload.

        We want the refresh token to be stored in a cookie not returned in the
        body along with the other data so we need to deserialize the payload,
        pop the token, set the cookie and reserialize the data before the
        return. Likewise, if we are requesting a new new access token with a
        refresh token (ie. when grant type is 'refresh_token') make sure to
        read the token data from the cookie.

        """
        data = request.POST.copy()
        data['client_secret'] = settings.OAUTH_CLIENT_SECRET
        if data['grant_type'] == 'refresh_token':
            refresh_token = request.COOKIES.get('refresh_token')
            data['refresh_token'] = refresh_token
        request.POST = data

        response = super().post(request, *args, **kwargs)

        data = json.loads(response.content.decode('utf-8'))
        refresh_token = data.pop('refresh_token')
        response.content = json.dumps(data).encode('utf-8')

        response.set_cookie(
            'refresh_token',
            refresh_token,
            max_age=settings.OAUTH2_REFRESH_TOKEN_COOKIE_EXPIRY,
            httponly=True,
            samesite='Lax',
            secure=not settings.IS_DEV,
        )

        return response
