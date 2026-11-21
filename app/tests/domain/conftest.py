"""Configure pytest for the tests.domain module."""

import pytest


@pytest.fixture
def preferences_view(db, current_tenant):  # noqa: ARG001
    """Inject the preferences viewset.

    Importing `domain.api` runs tenanted queries at class definition, so the
    import waits for the database and a bound tenant.

    """
    from domain.api.resources.preferences.endpoints import Preferences

    return Preferences


@pytest.fixture
def preference_key(db, factories):  # noqa: ARG001
    """Inject a preference key, which gives every user a preference for it."""
    return factories.preference_keys.create()
