"""Test the ida.management.commands.ensure_oauth module."""
import io
from unittest import mock

from oauth2_provider.models import Application

from django.core.management import call_command

from ida.management.commands.ensure_oauth import Command as EnsureOAuth


@mock.patch('ida.management.commands.ensure_oauth.io.StringIO')
@mock.patch('ida.management.commands.ensure_oauth.call_command')
@mock.patch('ida.management.commands.ensure_oauth.Application')
@mock.patch('ida.management.commands.ensure_oauth.logger')
def test_ensure_oauth_create_appliaction_some_failure(mock_logger, mock_application, mock_call_command, mock_io):
    mock_application.DoesNotExist = Application.DoesNotExist
    mock_application.objects.get.side_effect = Application.DoesNotExist('Some error')
    mock_io.return_value.__enter__.return_value.getvalue.return_value = 'Some error message'

    EnsureOAuth().handle()

    assert mock_application.mock_calls == [
        mock.call.objects.get(client_id='oauth.ida.development'),
    ]
    assert mock_call_command.mock_calls == [
        mock.call(
            'createapplication',
            'confidential',
            'authorization-code',
            stdout=mock_io.return_value.__enter__.return_value,
            client_id='oauth.ida.development',
            client_secret='django-insecure-development-environment-oauth-client-secret',
            algorithm='RS256',
            name='IDA',
            redirect_uris='http://dalme.localhost:8000/api/oauth/authorize/callback/ http://globalpharmacopeias.localhost:8000/api/oauth/authorize/callback/',
            skip_authorization=True,
        )
    ]
    assert mock_logger.mock_calls == [
        mock.call.error('Some error message'),
        mock.call.error('Failed to create oauth application'),
    ]


@mock.patch('ida.management.commands.ensure_oauth.io.StringIO')
@mock.patch('ida.management.commands.ensure_oauth.call_command')
@mock.patch('ida.management.commands.ensure_oauth.Application')
@mock.patch('ida.management.commands.ensure_oauth.logger')
def test_ensure_oauth_create(mock_logger, mock_application, mock_call_command, mock_io):
    mock_application.DoesNotExist = Application.DoesNotExist
    mock_application.objects.get.side_effect = Application.DoesNotExist('Some error')
    mock_io.return_value.__enter__.return_value.getvalue.return_value = 'New application IDA created successfully'

    EnsureOAuth().handle()

    assert mock_application.mock_calls == [
        mock.call.objects.get(client_id='oauth.ida.development'),
    ]
    assert mock_call_command.mock_calls == [
        mock.call(
            'createapplication',
            'confidential',
            'authorization-code',
            stdout=mock_io.return_value.__enter__.return_value,
            client_id='oauth.ida.development',
            client_secret='django-insecure-development-environment-oauth-client-secret',
            algorithm='RS256',
            name='IDA',
            redirect_uris='http://dalme.localhost:8000/api/oauth/authorize/callback/ http://globalpharmacopeias.localhost:8000/api/oauth/authorize/callback/',
            skip_authorization=True,
        )
    ]
    assert mock_logger.mock_calls == [
        mock.call.info('Created oauth application with client_id: %s', client_id='oauth.ida.development')
    ]


@mock.patch('ida.management.commands.ensure_oauth.call_command')
@mock.patch('ida.management.commands.ensure_oauth.Application')
@mock.patch('ida.management.commands.ensure_oauth.logger')
def test_ensure_oauth_refresh(mock_logger, mock_application, mock_call_command):
    out = io.StringIO()
    call_command('ensure_oauth', (), stdout=out, stderr=io.StringIO())

    assert out.getvalue() == ''
    assert mock_application.mock_calls == [
        mock.call.objects.get(client_id='oauth.ida.development'),
        mock.call.objects.get().save(),
    ]
    assert not mock_call_command.mock_calls
    assert mock_logger.mock_calls == [
        mock.call.info('Refreshed existing oauth application with client_id: %s', client_id='oauth.ida.development')
    ]