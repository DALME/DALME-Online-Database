"""Configure pytest for the tests.domain module."""

import pytest

from domain.models import PreferenceKey
from tenants.middleware.tenant_context_middleware import _tenant


@pytest.fixture
def current_tenant(test_tenant):
    """Bind the current tenant, as the tenant context middleware does per request."""
    token = _tenant.set(test_tenant)
    yield test_tenant
    _tenant.reset(token)


@pytest.fixture
def preferences_view(db, current_tenant):  # noqa: ARG001
    """Inject the preferences viewset.

    Importing `domain.api` runs tenanted queries at class definition, so the
    import waits for the database and a bound tenant.

    """
    from domain.api.resources.preferences.endpoints import Preferences

    return Preferences


@pytest.fixture
def preference_key(db):  # noqa: ARG001
    """Inject a preference key, which gives every user a preference for it."""
    return PreferenceKey.objects.create(
        name='theme',
        label='Theme',
        description='',
        data_type='STR',
        group='Record Editor',
        default='oneDark',
    )
