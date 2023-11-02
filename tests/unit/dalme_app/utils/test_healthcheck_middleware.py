"""Test the dalme_app.utils.healthcheck_middleware module."""
from http import HTTPStatus
from unittest import mock

from django.test import override_settings

from dalme_app.utils.healthcheck_middleware import HealthCheckMiddleware


def test_ping_endpoint_pass_through(rf):
    """Assert the health check passes through for any other URL."""
    request = rf.get('/some/other/route')
    get_response = mock.MagicMock()
    middleware = HealthCheckMiddleware(get_response)

    response = middleware(request)

    assert response == get_response.return_value


@override_settings(DEBUG=True)
@mock.patch('dalme_app.utils.healthcheck_middleware.MigrationExecutor')
def test_ping_endpoint_debug(mock_executor, rf):
    """Assert the health check passes in dev mode when there are no outstanding db migrations."""
    mock_executor.return_value.migration_plan.return_value = None
    request = rf.get('/api/healthcheck/')
    get_response = mock.MagicMock()
    middleware = HealthCheckMiddleware(get_response)

    response = middleware(request)

    assert response.content == b'{"detail": "OK"}'
    assert response.status_code == HTTPStatus.OK


@mock.patch('dalme_app.utils.healthcheck_middleware.MigrationExecutor')
def test_ping_endpoint_503s_when_db_not_ready(mock_executor, rf):
    """Assert the health check 503s when there are outstanding db migrations."""
    mock_executor.return_value.migration_plan.return_value = ['some plan data']
    request = rf.get('/api/healthcheck/')
    get_response = mock.MagicMock()
    middleware = HealthCheckMiddleware(get_response)

    response = middleware(request)

    assert response.content == b'{"detail": "Unhealthy"}'
    assert response.status_code == HTTPStatus.SERVICE_UNAVAILABLE


@mock.patch('dalme_app.utils.healthcheck_middleware.MigrationExecutor')
def test_ping_endpoint(mock_executor, rf):
    """Assert the health check passses when the db is up and ready."""
    mock_executor.return_value.migration_plan.return_value = None
    request = rf.get('/api/healthcheck/')
    get_response = mock.MagicMock()
    middleware = HealthCheckMiddleware(get_response)

    response = middleware(request)

    assert response.content == b'{"detail": "OK"}'
    assert response.status_code == HTTPStatus.OK
