"""Test the dalme_app.utils.multiple_proxy_middleware module."""
import re
from unittest import mock

from hypothesis import HealthCheck, given, settings
from hypothesis.provisional import domains
from hypothesis.strategies import lists

from django.test import RequestFactory

from dalme_app.utils.multiple_proxy_middleware import MultipleProxyMiddleware


@given(lists(elements=domains()).map(", ".join).filter(lambda x: bool(x)))
@settings(suppress_health_check=[HealthCheck.function_scoped_fixture])
def test_middleware(settings, ds):
    """Assert the middleware parses the correct host from a list.

    This middleware exists to ensure that `request.get_host` functions
    correctly further down the chain, so let's just assert over that invariant
    once it has been called.

    """
    settings.ALLOWED_HOSTS += [x.strip() for x in ds.split(",")]
    request = RequestFactory().get(
        "/",
        HTTP_X_FORWARDED_FOR=ds,
        HTTP_X_FORWARDED_HOST=ds,
        HTTP_X_FORWARDED_SERVER=ds,
    )

    get_response = mock.MagicMock()
    middleware = MultipleProxyMiddleware(get_response)
    middleware(request)

    assert request.get_host() == re.findall("^([^,]*)", ds)[0]
