"""Test the dalme_app.management.commands.collectstatic_tenants module."""
import argparse
import json
import os
from unittest import mock

import pytest

from django.core.management.base import CommandError

from dalme_app.management.commands.collectstatic_tenants import Command as CollectstaticTenants
from dalme_app.models import Tenant

MANIFEST_DATA = json.dumps(
    {
        'paths': {
            'some/js/file.js': 'some/js/file.034cc7d8a67f.js',
            'some/css/file.css': 'some/css/file.a2194c262648.css',
        },
        'version': '1.1',
        'hash': '2e773d792c4d',
    }
)


def test_collectstatic_tenants_args():
    """Test the argument handler for the command."""
    parser = argparse.ArgumentParser()
    CollectstaticTenants().add_arguments(parser)

    assert parser.parse_args(['--force', '--max-workers', '4']) == argparse.Namespace(force=True, max_workers=4)


@mock.patch.dict(os.environ, {'ENV': 'development'})
@mock.patch('dalme_app.management.commands.collectstatic_tenants.connection')
@mock.patch('dalme_app.management.commands.collectstatic_tenants.call_command')
@mock.patch('dalme_app.management.commands.collectstatic_tenants.Tenant')
@mock.patch('dalme_app.management.commands.collectstatic_tenants.logger')
def test_collectstatic_tenants_development(mock_logger, mock_tenant, mock_call_command, mock_connection):
    tenant_1 = mock.MagicMock(spec=Tenant)
    tenant_1.schema_name = 'tenant1'
    tenant_2 = mock.MagicMock(spec=Tenant)
    tenant_2.schema_name = 'tenant2'
    mock_tenant.objects.all.return_value = [tenant_1, tenant_2]

    CollectstaticTenants().handle()

    assert mock_call_command.called
    assert mock_connection.mock_calls == [
        mock.call.set_schema_to_public(),
    ]
    assert mock_logger.mock_calls == [
        mock.call.info('Collecting staticfiles for tenant: %s', tenant='public'),
        mock.call.info('Collecting staticfiles for tenant: %s', tenant='tenant1'),
        mock.call.info('Collecting staticfiles for tenant: %s', tenant='tenant2'),
    ]


@mock.patch.dict(os.environ, {'ENV': 'production'})
@mock.patch('dalme_app.management.commands.collectstatic_tenants.connection')
@mock.patch('dalme_app.management.commands.collectstatic_tenants.call_command')
@mock.patch('dalme_app.management.commands.collectstatic_tenants.Tenant')
@mock.patch('dalme_app.management.commands.collectstatic_tenants.logger')
def test_collectstatic_tenants_insufficient_workers(mock_logger, mock_tenant, mock_call_command, mock_connection):
    tenant_1 = mock.MagicMock(spec=Tenant)
    tenant_1.schema_name = 'tenant1'
    tenant_2 = mock.MagicMock(spec=Tenant)
    tenant_2.schema_name = 'tenant2'
    mock_tenant.objects.all.return_value = [tenant_1, tenant_2]

    with pytest.raises(CommandError) as exc:
        CollectstaticTenants().handle(max_workers=0)

    assert str(exc.value) == 'The maximum number of workers must be greater than 0.'

    assert not mock_call_command.called
    assert mock_connection.mock_calls == [
        mock.call.set_schema_to_public(),
    ]
    assert mock_logger.mock_calls == [
        mock.call.info('Collecting staticfiles for tenant: %s', tenant='public'),
    ]
