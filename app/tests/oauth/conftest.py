"""Configure pytest for the tests.oauth module."""

from datetime import UTC, datetime

import pytest

from django.conf import settings

from oauth.models import Application


@pytest.fixture
def oauth_application():
    """Inject an OAuth application."""
    client_id = settings.OAUTH_CLIENT_ID
    client_secret = settings.OAUTH_CLIENT_SECRET
    domains = ['http://dalme.localhost']
    redirect_uris = [f'{domain}/api/oauth/authorize/callback/' for domain in domains]
    post_logout_redirect_uris = [f'{domain}/' for domain in domains]
    kwargs = {
        'client_id': client_id,
        'client_secret': client_secret,
        'allowed_origins': ' '.join(domains),
        'redirect_uris': ' '.join(redirect_uris),
        'post_logout_redirect_uris': ' '.join(post_logout_redirect_uris),
        **settings.OAUTH2_APPLICATION_DEFAULTS,
    }

    return Application.objects.create(**kwargs)


@pytest.fixture
def unix_epoch_datetime():
    """Inject the Unix epoch datetime.

    Unix time 0 is exactly midnight UTC on 1 January 1970. It's a convenient
    instant to stub time predictably in tests, when time is irrelevant.

    """
    return datetime(1970, 1, 1, 0, 0, tzinfo=UTC)


@pytest.fixture
def unix_epoch_str():
    """Inject the datetime string for @freeze_time("1970-01-01").

    Unix time 0 is exactly midnight UTC on 1 January 1970. It's a convenient
    instant to stub time predictably in tests, when time is irrelevant.

    """
    return '1970-01-01T00:00:00Z'
