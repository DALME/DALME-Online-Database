"""Define validators for the OAuth module."""

from oauth2_provider.oauth2_validators import OAuth2Validator

from api.resources.groups import GroupSerializer
from app.context import get_current_tenant


class OAuth2Validator(OAuth2Validator):
    """Override the built-in OAuth claims response."""

    def get_userinfo_claims(self, request):
        """Enhance the default OIDC claims payload."""
        claims = super().get_userinfo_claims(request)
        avatar = request.user.avatar_url
        tenant = get_current_tenant()

        claims.update(
            {
                'avatar': avatar,
                'email': request.user.email,
                'username': request.user.username,
                'full_name': request.user.full_name,
                'is_admin': request.user.is_staff,
                'groups': GroupSerializer(request.user.groups_scoped, many=True).data,
                'tenant': {
                    'id': tenant.pk,
                    'name': tenant.name,
                },
            }
        )

        return claims
