"""Test the dalme_app.utils.ensure_superuser module."""
import os
from unittest import mock

import pytest

from django.contrib.auth.models import User

from dalme_app.management.commands.ensure_superuser import Command as EnsureSuperuser


@mock.patch.dict(os.environ, {'ADMIN_USERNAME': 'foo'})
@mock.patch('dalme_app.management.commands.ensure_superuser.User')
@mock.patch('dalme_app.management.commands.ensure_superuser.logger')
def test_ensure_superuser_no_creds(mock_logger, mock_user):
    with pytest.raises(KeyError) as exc:
        EnsureSuperuser().handle()

    assert str(exc.value) == "'ADMIN_PASSWORD'"

    assert mock_user.mock_calls == []
    assert mock_logger.mock_calls == [
        mock.call.exception('Missing admin user credentials in environment'),
    ]


@mock.patch.dict(os.environ, {'ADMIN_USERNAME': 'foo', 'ADMIN_PASSWORD': 'bar'})
@mock.patch('dalme_app.management.commands.ensure_superuser.User')
@mock.patch('dalme_app.management.commands.ensure_superuser.logger')
def test_ensure_superuser_create(mock_logger, mock_user):
    mock_user.DoesNotExist = User.DoesNotExist
    mock_user.objects.get.side_effect = User.DoesNotExist("Some error")

    EnsureSuperuser().handle()

    assert mock_user.mock_calls == [
        mock.call.objects.get(username='foo'),
        mock.call.objects.create(
            username='foo', password='bar', is_superuser=True,
        ),
    ]
    assert mock_logger.mock_calls == [
        mock.call.info('Created superuser', user='foo'),
    ]


@mock.patch.dict(os.environ, {'ADMIN_USERNAME': 'foo', 'ADMIN_PASSWORD': 'bar'})
@mock.patch('dalme_app.management.commands.ensure_superuser.User')
@mock.patch('dalme_app.management.commands.ensure_superuser.logger')
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
