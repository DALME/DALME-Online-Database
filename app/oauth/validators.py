"""Define validators for the OAuth module."""

from oauth2_provider.oauth2_validators import OAuth2Validator

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
                'date_joined': request.user.date_joined.isoformat() if request.user.date_joined else None,
                'email': request.user.email,
                'first_name': request.user.first_name,
                'full_name': request.user.full_name,
                'groupIds': [g.id for g in request.user.groups_scoped],
                'is_active': request.user.is_active,
                'is_staff': request.user.is_staff,
                'is_superuser': request.user.is_superuser,
                'last_login': request.user.last_login.isoformat() if request.user.last_login else None,
                'last_name': request.user.last_name,
                'username': request.user.username,
                'tenant': {
                    'id': tenant.pk,
                    'name': tenant.name,
                },
            }
        )

        return claims
