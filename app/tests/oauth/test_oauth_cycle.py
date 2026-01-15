"""Test the oauth authentication API."""

import base64
import hashlib
import random
import string
from unittest import mock
from urllib.parse import urlencode

import jwt
import pytest
from freezegun import freeze_time
from oauth2_provider.settings import DEFAULTS as OAUTH_DEFAULTS
from rest_framework import status

from django.test import Client
from django.urls import reverse


@freeze_time('1970-01-01')
@pytest.mark.urls('app.urls.urls_tenant')
@pytest.mark.django_db
@mock.patch('tenants.middleware.tenant_middleware.Domain')
def test_oauth_complete_cycle(  # noqa: PLR0915
    mock_domain,
    settings,
    test_username,
    test_password,
    unix_epoch_datetime,
    user,
    oauth_application,
    log,
    test_domain,
):
    """A full integration test for the authorization code flow procedure.

    This is quite an expansive test. But OAuth is complex and important so we
    really want to expose and exercise as much of the flow and the surrounding
    logic as possible, at least here and additionally with an end-to-end test.

    https://django-oauth-toolkit.readthedocs.io/en/latest/getting_started.html#authorization-code

    """
    mock_domain.objects.select_related.return_value.get.return_value = test_domain
    client = Client(HTTP_HOST=test_domain.domain)

    assert oauth_application.allowed_origins == f'http://{test_domain.domain}'

    # Let's accumulate the logs emitted per request so we can just check the
    # diff as they appear after each event.
    expected_logs = []
    assert log.events == expected_logs

    # This will be denied because we are not authenticated at all.
    url = reverse('api:users-detail', kwargs={'pk': user.id})
    response = client.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN

    expected_logs = [
        *expected_logs,
        {
            'request': f'GET {url}',
            'user_agent': None,
            'event': 'request_started',
            'domain': test_domain.domain,
            'tenant': mock.ANY,
            'ip': '127.0.0.1',
            'request_id': mock.ANY,
            'level': 'info',
        },
        {
            'request': f'GET {url}',
            'user_agent': None,
            'event': 'request_started',
            'domain': test_domain.domain,
            'tenant': mock.ANY,
            'ip': '127.0.0.1',
            'request_id': mock.ANY,
            'level': 'info',
        },
        {
            'code': status.HTTP_403_FORBIDDEN,
            'request': f'GET {url}',
            'event': 'request_finished',
            'domain': test_domain.domain,
            'tenant': mock.ANY,
            'ip': '127.0.0.1',
            'user_id': None,
            'request_id': mock.ANY,
            'level': 'warning',
        },
        {
            'code': status.HTTP_403_FORBIDDEN,
            'request': f'GET {url}',
            'event': 'request_finished',
            'user_id': None,
            'level': 'warning',
        },
    ]

    assert log.events == expected_logs

    # Login to the Django session with the user's credentials.
    url = reverse('oauth:login')
    response = client.post(
        url,
        {
            'username': test_username,
            'password': test_password,
        },
        content_type='application/json',
    )
    user.refresh_from_db()

    assert response.status_code == status.HTTP_202_ACCEPTED
    assert user.last_login == unix_epoch_datetime
    assert response.wsgi_request.session['_auth_user_id'] == str(user.pk)

    expected_logs = [
        *expected_logs,
        {
            'request': f'POST {url}',
            'user_agent': None,
            'event': 'request_started',
            'domain': test_domain.domain,
            'ip': '127.0.0.1',
            'tenant': mock.ANY,
            'request_id': mock.ANY,
            'level': 'info',
        },
        {
            'request': f'POST {url}',
            'user_agent': None,
            'event': 'request_started',
            'domain': test_domain.domain,
            'ip': '127.0.0.1',
            'tenant': mock.ANY,
            'request_id': mock.ANY,
            'level': 'info',
        },
        {
            'user': user,
            'event': 'User successfully logged in',
            'domain': test_domain.domain,
            'ip': '127.0.0.1',
            'tenant': mock.ANY,
            'request_id': mock.ANY,
            'level': 'info',
        },
        {
            'code': status.HTTP_202_ACCEPTED,
            'request': f'POST {url}',
            'event': 'request_finished',
            'domain': test_domain.domain,
            'user_id': user.id,
            'ip': '127.0.0.1',
            'tenant': mock.ANY,
            'request_id': mock.ANY,
            'level': 'info',
        },
        {
            'code': status.HTTP_202_ACCEPTED,
            'request': f'POST {url}',
            'event': 'request_finished',
            'user_id': user.id,
            'level': 'info',
        },
    ]
    assert log.events == expected_logs

    # Now we can fetch the auth user, but that's just by virtue of being logged
    # into a session and not because of any OAuth procedure itself.
    url = reverse('api:users-detail', kwargs={'pk': user.id})
    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == test_username

    expected_logs = [
        *expected_logs,
        {
            'request': f'GET {url}',
            'user_agent': None,
            'event': 'request_started',
            'tenant': mock.ANY,
            'request_id': mock.ANY,
            'ip': '127.0.0.1',
            'domain': test_domain.domain,
            'level': 'info',
        },
        {
            'request': f'GET {url}',
            'user_agent': None,
            'event': 'request_started',
            'tenant': mock.ANY,
            'request_id': mock.ANY,
            'ip': '127.0.0.1',
            'domain': test_domain.domain,
            'level': 'info',
        },
        {
            'code': status.HTTP_200_OK,
            'request': f'GET {url}',
            'event': 'request_finished',
            'user_id': user.id,
            'tenant': mock.ANY,
            'request_id': mock.ANY,
            'ip': '127.0.0.1',
            'domain': test_domain.domain,
            'level': 'info',
        },
        {
            'code': status.HTTP_200_OK,
            'request': f'GET {url}',
            'event': 'request_finished',
            'user_id': user.id,
            'level': 'info',
        },
    ]
    assert log.events == expected_logs

    # Let's generate an OAauth access token. A few requests are necessary.
    # This code challenge logic will actually happen in the SPA/frontend but
    # we'll do it here for these tests as we are not in an end-to-end harness.
    code_verifier = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128))
    )
    hashed_verifier = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(hashed_verifier).decode('utf-8').replace('=', '')

    # PKCE machinery.
    pkce_payload = {
        'response_type': 'code',
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256',
        'client_id': settings.OAUTH_CLIENT_ID,
        'redirect_uri': f'http://{test_domain.domain}/api/oauth/authorize/callback/',
    }
    url = reverse('oauth:authorize')
    response = client.get(url, pkce_payload)

    # The PKCE code is delivered to us via a 302 redirect URL with a query
    # parameter containing the code. We extract it here so we can proceed.
    assert response.status_code == status.HTTP_302_FOUND
    assert 'code' in response.url  # type: ignore[attr-defined]
    _, code = response.url.split('code=')  # type: ignore[attr-defined]

    expected_logs = [
        *expected_logs,
        {
            'request': f'GET {url}?{urlencode(pkce_payload)}',
            'user_agent': None,
            'event': 'request_started',
            'ip': '127.0.0.1',
            'tenant': mock.ANY,
            'domain': test_domain.domain,
            'request_id': mock.ANY,
            'level': 'info',
        },
        {
            'request': f'GET {url}?{urlencode(pkce_payload)}',
            'user_agent': None,
            'event': 'request_started',
            'ip': '127.0.0.1',
            'tenant': mock.ANY,
            'domain': test_domain.domain,
            'request_id': mock.ANY,
            'level': 'info',
        },
        {
            'code': status.HTTP_302_FOUND,
            'request': f'GET {url}?{urlencode(pkce_payload)}',
            'event': 'request_finished',
            'ip': '127.0.0.1',
            'tenant': mock.ANY,
            'user_id': user.id,
            'domain': test_domain.domain,
            'request_id': mock.ANY,
            'level': 'info',
        },
        {
            'code': status.HTTP_302_FOUND,
            'request': f'GET {url}?{urlencode(pkce_payload)}',
            'event': 'request_finished',
            'user_id': user.id,
            'level': 'info',
        },
    ]
    assert log.events == expected_logs

    # We don't *need* to hit this endpoint, just having the redirect URL with
    # the code on it is enough, but it will exercise that view for us if we do,
    # so let's do that and we score an easy regression test.
    response = client.get(response.url)  # type: ignore[attr-defined]
    assert response.status_code == status.HTTP_200_OK

    expected_logs = [
        *expected_logs,
        {
            'request': f'GET /api/oauth/authorize/callback/?code={code}',
            'user_agent': None,
            'event': 'request_started',
            'ip': '127.0.0.1',
            'level': 'info',
            'request_id': mock.ANY,
            'tenant': mock.ANY,
            'domain': test_domain.domain,
        },
        {
            'request': f'GET /api/oauth/authorize/callback/?code={code}',
            'user_agent': None,
            'event': 'request_started',
            'ip': '127.0.0.1',
            'level': 'info',
            'request_id': mock.ANY,
            'tenant': mock.ANY,
            'domain': test_domain.domain,
        },
        {
            'code': status.HTTP_200_OK,
            'event': 'request_finished',
            'ip': '127.0.0.1',
            'level': 'info',
            'request': f'GET /api/oauth/authorize/callback/?code={code}',
            'request_id': mock.ANY,
            'tenant': mock.ANY,
            'domain': test_domain.domain,
            'user_id': user.id,
        },
        {
            'code': status.HTTP_200_OK,
            'event': 'request_finished',
            'level': 'info',
            'request': f'GET /api/oauth/authorize/callback/?code={code}',
            'user_id': user.id,
        },
    ]
    assert log.events == expected_logs

    # Now we can try and get an actual OAuth access token.
    url = reverse('oauth:token')
    response = client.post(
        url,
        urlencode(
            {
                # We omit the `client_secret` as it's handled by the server.
                'client_id': settings.OAUTH_CLIENT_ID,
                'code': code,
                'code_verifier': code_verifier,
                'grant_type': 'authorization_code',
                'redirect_uri': f'http://{test_domain.domain}/api/oauth/authorize/callback/',
            }
        ),
        content_type='application/x-www-form-urlencoded',
        headers={'Cache-Control': 'no-cache'},
    )
    authorization_payload = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert authorization_payload == {
        'access_token': mock.ANY,
        'expires_in': int(settings.OAUTH2_ACCESS_TOKEN_EXPIRY),
        'token_type': 'Bearer',
        'scope': ' '.join(settings.OAUTH2_SCOPES.keys()),
        'id_token': mock.ANY,
    }

    # Ensure the `refresh_token` is baked into the cookies.
    assert 'refresh_token' not in authorization_payload
    assert response.cookies.get('refresh_token')

    # Let's check the JWT claims held by the `id_token`.
    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1

    assert jwt.decode(authorization_payload['id_token'], options={'verify_signature': False}) == {
        'aud': settings.OAUTH_CLIENT_ID,
        'iat': 0,
        'at_hash': mock.ANY,
        'sub': str(user.id),
        'iss': f'http://{test_domain.domain}/api/oauth',
        'exp': OAUTH_DEFAULTS['ID_TOKEN_EXPIRE_SECONDS'],
        'auth_time': 0,
        'jti': mock.ANY,  # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.7
    }

    expected_logs = [
        *expected_logs,
        {
            'event': 'request_started',
            'ip': '127.0.0.1',
            'level': 'info',
            'request': f'POST {url}',
            'request_id': mock.ANY,
            'user_agent': None,
            'tenant': mock.ANY,
            'domain': test_domain.domain,
        },
        {
            'event': 'request_started',
            'ip': '127.0.0.1',
            'level': 'info',
            'request': f'POST {url}',
            'request_id': mock.ANY,
            'user_agent': None,
            'tenant': mock.ANY,
            'domain': test_domain.domain,
        },
        {
            'code': status.HTTP_200_OK,
            'event': 'request_finished',
            'ip': '127.0.0.1',
            'level': 'info',
            'request': f'POST {url}',
            'request_id': mock.ANY,
            'user_id': user.id,
            'tenant': mock.ANY,
            'domain': test_domain.domain,
        },
        {
            'code': status.HTTP_200_OK,
            'event': 'request_finished',
            'level': 'info',
            'user_id': user.id,
            'request': f'POST {url}',
        },
    ]
    assert log.events == expected_logs

    # Now, let's fetch the auth user via an Ajax request. This will require the
    # token to be included and the right headers to be set.
    url = reverse('api:users-detail', kwargs={'pk': user.id})
    response = client.get(
        url,
        headers={
            'Authorization': f'{authorization_payload["token_type"]} {authorization_payload["access_token"]}',
            'X-Requested-With': 'XMLHttpRequest',
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == test_username

    expected_logs = [
        *expected_logs,
        {
            'event': 'request_started',
            'ip': '127.0.0.1',
            'level': 'info',
            'request': f'GET {url}',
            'request_id': mock.ANY,
            'user_agent': None,
            'tenant': mock.ANY,
            'domain': test_domain.domain,
        },
        {
            'event': 'request_started',
            'ip': '127.0.0.1',
            'level': 'info',
            'request': f'GET {url}',
            'request_id': mock.ANY,
            'user_agent': None,
            'tenant': mock.ANY,
            'domain': test_domain.domain,
        },
        {
            'code': status.HTTP_200_OK,
            'event': 'request_finished',
            'ip': '127.0.0.1',
            'level': 'info',
            'request': f'GET {url}',
            'request_id': mock.ANY,
            'user_id': user.id,
            'tenant': mock.ANY,
            'domain': test_domain.domain,
        },
        {
            'code': status.HTTP_200_OK,
            'event': 'request_finished',
            'level': 'info',
            'request': f'GET {url}',
            'user_id': user.id,
        },
    ]
    assert log.events == expected_logs

    # Generate a new access token via the refresh cycle. The `refresh_token` is
    # in the cookie so we don't need to include that anywhere in the request,
    # it's handled by the endpoint itself.
    url = reverse('oauth:token')
    response = client.post(
        url,
        urlencode(
            {
                # Again, we can omit the `client_secret`.
                'client_id': settings.OAUTH_CLIENT_ID,
                'grant_type': 'refresh_token',
            }
        ),
        content_type='application/x-www-form-urlencoded',
        headers={'Cache-Control': 'no-cache'},
    )
    refresh_payload = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert refresh_payload == {
        'access_token': mock.ANY,
        'expires_in': int(settings.OAUTH2_ACCESS_TOKEN_EXPIRY),
        'token_type': 'Bearer',
        'scope': ' '.join(settings.OAUTH2_SCOPES.keys()),
        'id_token': mock.ANY,
    }
    assert authorization_payload['access_token'] != refresh_payload['access_token']

    expected_logs = [
        *expected_logs,
        {
            'event': 'request_started',
            'ip': '127.0.0.1',
            'level': 'info',
            'request': f'POST {url}',
            'request_id': mock.ANY,
            'user_agent': None,
            'tenant': mock.ANY,
            'domain': test_domain.domain,
        },
        {
            'event': 'request_started',
            'ip': '127.0.0.1',
            'level': 'info',
            'request': f'POST {url}',
            'request_id': mock.ANY,
            'user_agent': None,
            'tenant': mock.ANY,
            'domain': test_domain.domain,
        },
        {
            'code': status.HTTP_200_OK,
            'event': 'request_finished',
            'ip': '127.0.0.1',
            'level': 'info',
            'request': f'POST {url}',
            'request_id': mock.ANY,
            'user_id': user.id,
            'tenant': mock.ANY,
            'domain': test_domain.domain,
        },
        {
            'code': status.HTTP_200_OK,
            'event': 'request_finished',
            'level': 'info',
            'request': f'POST {url}',
            'user_id': user.id,
        },
    ]
    assert log.events == expected_logs

    # Using OAuth we can still fetch the auth user as we would expect.
    url = reverse('api:users-detail', kwargs={'pk': user.id})
    response = client.get(
        url,
        headers={
            'Authorization': f'{refresh_payload["token_type"]} {refresh_payload["access_token"]}',
            'X-Requested-With': 'XMLHttpRequest',
        },
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['username'] == test_username

    expected_logs = [
        *expected_logs,
        {
            'event': 'request_started',
            'ip': '127.0.0.1',
            'level': 'info',
            'request': f'GET {url}',
            'request_id': mock.ANY,
            'user_agent': None,
            'tenant': mock.ANY,
            'domain': test_domain.domain,
        },
        {
            'event': 'request_started',
            'ip': '127.0.0.1',
            'level': 'info',
            'request': f'GET {url}',
            'request_id': mock.ANY,
            'user_agent': None,
            'tenant': mock.ANY,
            'domain': test_domain.domain,
        },
        {
            'code': status.HTTP_200_OK,
            'event': 'request_finished',
            'ip': '127.0.0.1',
            'level': 'info',
            'request': f'GET {url}',
            'request_id': mock.ANY,
            'user_id': user.id,
            'tenant': mock.ANY,
            'domain': test_domain.domain,
        },
        {
            'code': status.HTTP_200_OK,
            'event': 'request_finished',
            'level': 'info',
            'request': f'GET {url}',
            'user_id': user.id,
        },
    ]
    assert log.events == expected_logs

    # Try fetching the auth user with an Ajax request but without a token and
    # it won't succeed, because the `access_token` is the carrier of OAuth.
    url = reverse('api:users-detail', kwargs={'pk': user.id})
    response = client.get(
        url,
        headers={
            'X-Requested-With': 'XMLHttpRequest',
        },
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

    expected_logs = [
        *expected_logs,
        {
            'event': 'request_started',
            'ip': '127.0.0.1',
            'level': 'info',
            'request': f'GET {url}',
            'request_id': mock.ANY,
            'user_agent': None,
            'tenant': mock.ANY,
            'domain': test_domain.domain,
        },
        {
            'event': 'request_started',
            'ip': '127.0.0.1',
            'level': 'info',
            'request': f'GET {url}',
            'request_id': mock.ANY,
            'user_agent': None,
            'tenant': mock.ANY,
            'domain': test_domain.domain,
        },
        {
            'code': status.HTTP_401_UNAUTHORIZED,
            'event': 'request_finished',
            'ip': '127.0.0.1',
            'level': 'warning',
            'request': f'GET {url}',
            'request_id': mock.ANY,
            'user_id': None,
            'tenant': mock.ANY,
            'domain': test_domain.domain,
        },
        {
            'code': status.HTTP_401_UNAUTHORIZED,
            'event': 'request_finished',
            'level': 'warning',
            'request': f'GET {url}',
            'user_id': None,
        },
    ]
    assert log.events == expected_logs
