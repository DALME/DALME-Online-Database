"""Test that responses carry the Permissions-Policy header."""

import pytest

from django.test import Client


@pytest.mark.django_db
def test_responses_deny_unused_browser_features(test_domain):
    response = Client(HTTP_HOST=test_domain.domain).get('/api/preferences/')

    policy = response.headers.get('Permissions-Policy', '')
    assert 'camera=()' in policy
    assert 'geolocation=()' in policy
    assert 'microphone=()' in policy


@pytest.mark.django_db
def test_the_sites_own_pages_may_go_full_screen(test_domain):
    response = Client(HTTP_HOST=test_domain.domain).get('/api/preferences/')

    assert 'fullscreen=(self)' in response.headers.get('Permissions-Policy', '')
