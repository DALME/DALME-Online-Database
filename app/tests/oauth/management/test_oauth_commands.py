"""Test the oauth management commands."""

import io
import os
from unittest import mock

import pytest
from oauth2_provider.models import Application

from django.core.management import call_command
from django.test import override_settings

from oauth.management.commands.ensure_oauth import Command as EnsureOAuth
from oauth.management.commands.ensure_superuser import Command as EnsureSuperuser
from oauth.models import User

EXPECTED_TENANTS = ['ida', 'dalme', 'pharmacopeias']


@mock.patch('oauth.management.commands.ensure_oauth.io.StringIO')
@mock.patch('oauth.management.commands.ensure_oauth.call_command')
@mock.patch('oauth.management.commands.ensure_oauth.Application')
def test_ensure_oauth_create_application_some_failure(mock_application, mock_call_command, mock_io, log):
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
            redirect_uris=' '.join(
                f'http://{tenant}.localhost:8000/api/oauth/authorize/callback/' for tenant in EXPECTED_TENANTS
            ),
            post_logout_redirect_uris=' '.join(f'http://{tenant}.localhost:8000/' for tenant in EXPECTED_TENANTS),
            skip_authorization=True,
        )
    ]
    assert log.events == [
        {'event': 'Some error message', 'level': 'error'},
        {'event': 'Failed to create oauth application', 'level': 'error'},
    ]


@mock.patch('oauth.management.commands.ensure_oauth.io.StringIO')
@mock.patch('oauth.management.commands.ensure_oauth.call_command')
@mock.patch('oauth.management.commands.ensure_oauth.Application')
def test_ensure_oauth_create(mock_application, mock_call_command, mock_io, log):
    mock_oauth_application = mock.MagicMock(spec=Application)
    mock_application.DoesNotExist = Application.DoesNotExist
    mock_application.objects.get.side_effect = [Application.DoesNotExist('Some error'), mock_oauth_application]
    mock_io.return_value.__enter__.return_value.getvalue.return_value = 'New application IDA created successfully'

    EnsureOAuth().handle()

    assert mock_application.mock_calls == [
        mock.call.objects.get(client_id='oauth.ida.development'),
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
            redirect_uris=' '.join(
                f'http://{tenant}.localhost:8000/api/oauth/authorize/callback/' for tenant in EXPECTED_TENANTS
            ),
            post_logout_redirect_uris=' '.join(f'http://{tenant}.localhost:8000/' for tenant in EXPECTED_TENANTS),
            skip_authorization=True,
        )
    ]
    assert mock_oauth_application.allowed_origins == ' '.join(
        f'http://{tenant}.localhost:8000' for tenant in EXPECTED_TENANTS
    )
    assert mock_oauth_application.mock_calls == [
        mock.call.save(),
    ]
    assert log.events == [
        {
            'event': 'Created oauth application with client_id: %s',
            'client_id': 'oauth.ida.development',
            'level': 'info',
        },
    ]


@mock.patch('oauth.management.commands.ensure_oauth.call_command')
@mock.patch('oauth.management.commands.ensure_oauth.Application')
def test_ensure_oauth_refresh(mock_application, mock_call_command, log):
    out = io.StringIO()
    call_command('ensure_oauth', (), stdout=out, stderr=io.StringIO())

    assert out.getvalue() == ''
    assert mock_application.mock_calls == [
        mock.call.objects.get(client_id='oauth.ida.development'),
        mock.call.objects.get().save(),
    ]
    assert not mock_call_command.mock_calls
    assert log.events == [
        {
            'event': 'Refreshed existing oauth application with client_id: %s',
            'client_id': 'oauth.ida.development',
            'level': 'info',
        }
    ]


@mock.patch.dict(os.environ, {'ADMIN_USERNAME': 'test@example.com'})
@override_settings(ENV='production')
def test_ensure_superuser_no_creds(log):
    with pytest.raises(KeyError) as exc:
        EnsureSuperuser().handle()

    assert str(exc.value) == "'ADMIN_PASSWORD'"

    assert log.events == [
        {
            'event': 'Missing admin user credentials in environment',
            'level': 'error',
            'exc_info': True,
        }
    ]


@mock.patch.dict(os.environ, {'ADMIN_USERNAME': 'foo', 'ADMIN_PASSWORD': 'bar'})
@mock.patch('oauth.management.commands.ensure_superuser.User')
@mock.patch('oauth.management.commands.ensure_superuser.logger')
def test_ensure_superuser_create(mock_logger, mock_user):
    mock_user.DoesNotExist = User.DoesNotExist
    mock_user.objects.get.side_effect = User.DoesNotExist('Some error')

    EnsureSuperuser().handle()

    assert mock_user.mock_calls == [
        mock.call.objects.get(username='foo'),
        mock.call.objects.create(
            username='foo',
            password='bar',
            is_superuser=True,
        ),
    ]
    assert mock_logger.mock_calls == [
        mock.call.info('Created superuser', user='foo'),
    ]


@mock.patch.dict(os.environ, {'ADMIN_USERNAME': 'foo', 'ADMIN_PASSWORD': 'bar'})
@mock.patch('oauth.management.commands.ensure_superuser.User')
@mock.patch('oauth.management.commands.ensure_superuser.logger')
def test_ensure_superuser_refresh(mock_logger, mock_user):
    EnsureSuperuser().handle()

    assert mock_user.mock_calls == [
        mock.call.objects.get(username='foo'),
        mock.call.objects.get().set_password('bar'),
        mock.call.objects.get().save(),
    ]
    assert mock_logger.mock_calls == [
        mock.call.info('Refreshed password for superuser', user='foo'),
    ]
