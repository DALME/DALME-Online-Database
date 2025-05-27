"""Define the authentication API."""

import json

import structlog
from oauth2_provider.views import TokenView
from rest_framework import permissions, status, views
from rest_framework.response import Response

from django.conf import settings
from django.contrib.auth import login

from app.access_policies import BaseAccessPolicy
from oauth.serializers import LoginSerializer

logger = structlog.get_logger(__name__)


class AuthAccessPolicy(BaseAccessPolicy):
    """Access policies for authorization and authentication."""

    id = 'auth-policy'


class AuthorizationCode(views.APIView):
    """API endpoint that receives the OIDC authorization token."""

    def get(self, request):  # noqa: ARG002
        return Response(None, status=status.HTTP_200_OK)


class Login(views.APIView):
    """API endpoint for session authentication login."""

    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):  # noqa: A002, ARG002
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        login(request, user)

        logger.info('User successfully logged in', user=user)
        return Response(None, status=status.HTTP_202_ACCEPTED)


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

        if response.status_code == status.HTTP_200_OK:
            data = json.loads(response.content.decode('utf-8'))
            refresh_token = data.pop('refresh_token')
            response.content = json.dumps(data).encode('utf-8')

            response.set_cookie(
                'refresh_token',
                refresh_token,
                max_age=int(settings.OAUTH2_REFRESH_TOKEN_COOKIE_EXPIRY),
                httponly=True,
                samesite='Lax',
                secure=not settings.IS_DEV,
            )

        return response
