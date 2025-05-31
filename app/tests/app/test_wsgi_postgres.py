"""Tests for the WSGI application setup."""

from unittest import mock


@mock.patch('configurations.wsgi.get_wsgi_application')
def test_application_is_callable(mock_get_wsgi_application):
    # Patch get_wsgi_application to return a dummy callable
    def dummy_app(environ, start_response):  # noqa: ARG001
        return None

    mock_get_wsgi_application.return_value = dummy_app
    from app import wsgi

    assert callable(wsgi.application)


@mock.patch('django.conf.settings.SQL_TIMEOUT', 30000)
def test_setup_postgres_sets_timeout():
    # Prepare a mock connection
    mock_cursor = mock.MagicMock()
    mock_connection = mock.MagicMock()
    mock_connection.vendor = 'postgresql'
    mock_connection.cursor.return_value.__enter__.return_value = mock_cursor

    # Import the setup_postgres function
    from app import wsgi

    wsgi.setup_postgres(mock_connection)

    mock_cursor.execute.assert_called_once_with('SET statement_timeout TO %s;', [30000])


def test_setup_postgres_when_not_postgres():
    # Prepare a mock connection with a different vendor
    mock_connection = mock.MagicMock()
    mock_connection.vendor = 'sqlite'
    mock_connection.cursor.return_value.__enter__.return_value = mock.MagicMock()

    from app import wsgi

    wsgi.setup_postgres(mock_connection)

    # cursor should not be called for non-postgresql
    assert not mock_connection.cursor.called
