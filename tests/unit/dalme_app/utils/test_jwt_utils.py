"""Test the dalme_app.utils.jwt_utils module."""
from unittest import mock

from django.contrib.auth import get_user_model

from dalme_app.models import Tenant
from dalme_app.utils.jwt_utils import JWTSessionAuthentication


@mock.patch('dalme_app.utils.jwt_utils.get_current_tenant')
@mock.patch('dalme_app.utils.jwt_utils.JWTSessionAuthentication.create_session')
@mock.patch('dalme_app.utils.jwt_utils.auth')
@mock.patch('dalme_app.utils.jwt_utils.TenantRole.objects')
def test_middleware(
    mock_tenant_role_objs,
    mock_auth,
    mock_create_session,
    mock_get_tenant,
    rf,
):
    """Assert the middleware handles authentication correctly."""
    User = get_user_model()  # noqa: N806
    mock_user = mock.MagicMock(spec=User)
    mock_user.is_active = True
    mock_auth.authenticate.return_value = mock_user
    mock_tenant = mock.MagicMock(spec=Tenant)
    mock_get_tenant.return_value = mock_tenant
    mock_tenant_role_objs.filter.return_value = mock_tenant_role_objs
    mock_tenant_role_objs.exists.return_value = True

    request = rf.post(
        '/api/jwt/login/',
        {'username': 'foo', 'password': 'bar'},
        content_type='application/json',
    )
    request.tenant = mock_tenant
    request.user = mock_user

    get_response = mock.MagicMock()
    middleware = JWTSessionAuthentication(get_response)
    middleware(request)

    assert mock_auth.mock_calls == [
        mock.call.authenticate(request, username='foo', password='bar'),
        mock.call.login(request, mock_user),
    ]
    assert mock_tenant_role_objs.mock_calls == [
        mock.call.filter(user=mock_user, tenant=mock_tenant),
        mock.call.exists(),
    ]
    assert mock_create_session.mock_calls == [
        mock.call(request, mock_user),
    ]
