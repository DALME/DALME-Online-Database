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


@mock.patch.dict(os.environ, {'ENV': 'production'})
@mock.patch('dalme_app.management.commands.collectstatic_tenants.staticfiles_storage')
@mock.patch('dalme_app.management.commands.collectstatic_tenants.call_command')
@mock.patch('dalme_app.management.commands.collectstatic_tenants.Tenant')
@mock.patch('dalme_app.management.commands.collectstatic_tenants.logger')
def test_collectstatic_tenants_does_not_exist(mock_logger, mock_tenant, mock_call_command, mock_storage):
    tenant_1 = mock.MagicMock(spec=Tenant)
    tenant_1.schema_name = 'tenant1'
    tenant_2 = mock.MagicMock(spec=Tenant)
    tenant_2.schema_name = 'tenant2'
    mock_tenant.objects.all.return_value = [tenant_1, tenant_2]
    mock_storage.exists.return_value = False

    with mock.patch(
        'dalme_app.management.commands.collectstatic_tenants.open_rb',
        mock.mock_open(read_data=MANIFEST_DATA),
    ) as mock_open:
        CollectstaticTenants().handle()

        assert mock_open.call_count == 12  # noqa: PLR2004

    assert mock_call_command.called

    # The order is non-deterministic in the following data because of the
    # threading pool so we can just loop instead to account for eveything.
    for call in [
        mock.call.exists('staticfiles.json'),
        mock.call.save('some/css/file.a2194c262648.css', mock_open.return_value),
        mock.call.save('some/js/file.034cc7d8a67f.js', mock_open.return_value),
        mock.call.save('staticfiles.json', mock_open.return_value),
    ]:
        assert call in mock_storage.mock_calls

    for call in [
        mock.call.info('Collecting staticfiles for tenant: %s', tenant='public'),
        mock.call.info('Uploading %s files for tenant: %s', count=2, tenant='public'),
        mock.call.info('File was uploaded to: %s/%s', tenant='public', path='some/js/file.034cc7d8a67f.js'),
        mock.call.info('File was uploaded to: %s/%s', tenant='public', path='some/css/file.a2194c262648.css'),
        mock.call.info('Uploading the manifest for tenant: %s', tenant='public'),
        mock.call.info('Collecting staticfiles for tenant: %s', tenant='tenant1'),
        mock.call.info('Uploading %s files for tenant: %s', count=2, tenant='tenant1'),
        mock.call.info('File was uploaded to: %s/%s', tenant='tenant1', path='some/js/file.034cc7d8a67f.js'),
        mock.call.info('File was uploaded to: %s/%s', tenant='tenant1', path='some/css/file.a2194c262648.css'),
        mock.call.info('Uploading the manifest for tenant: %s', tenant='tenant1'),
        mock.call.info('Collecting staticfiles for tenant: %s', tenant='tenant2'),
        mock.call.info('Uploading %s files for tenant: %s', count=2, tenant='tenant2'),
        mock.call.info('File was uploaded to: %s/%s', tenant='tenant2', path='some/js/file.034cc7d8a67f.js'),
        mock.call.info('File was uploaded to: %s/%s', tenant='tenant2', path='some/css/file.a2194c262648.css'),
        mock.call.info('Uploading the manifest for tenant: %s', tenant='tenant2'),
    ]:
        assert call in mock_logger.mock_calls


@mock.patch.dict(os.environ, {'ENV': 'production'})
@mock.patch('dalme_app.management.commands.collectstatic_tenants.staticfiles_storage')
@mock.patch('dalme_app.management.commands.collectstatic_tenants.call_command')
@mock.patch('dalme_app.management.commands.collectstatic_tenants.Tenant')
@mock.patch('dalme_app.management.commands.collectstatic_tenants.logger')
def test_collectstatic_tenants_exists(mock_logger, mock_tenant, mock_call_command, mock_storage):
    tenant_1 = mock.MagicMock(spec=Tenant)
    tenant_1.schema_name = 'tenant1'
    tenant_2 = mock.MagicMock(spec=Tenant)
    tenant_2.schema_name = 'tenant2'
    mock_tenant.objects.all.return_value = [tenant_1, tenant_2]
    mock_storage.exists.return_value = True

    with mock.patch(
        'dalme_app.management.commands.collectstatic_tenants.open_rb', mock.mock_open(read_data=MANIFEST_DATA)
    ) as mock_open:
        CollectstaticTenants().handle()

        assert mock_open.call_count == 9  # noqa: PLR2004

    assert mock_call_command.called

    assert mock_storage.mock_calls == [
        # public
        mock.call.exists('staticfiles.json'),
        mock.call.save('staticfiles.json', mock_open.return_value),
        # tenant1
        mock.call.exists('staticfiles.json'),
        mock.call.save('staticfiles.json', mock_open.return_value),
        # tenant2
        mock.call.exists('staticfiles.json'),
        mock.call.save('staticfiles.json', mock_open.return_value),
    ]

    # The order is non-deterministic in the following data because of the
    # threading pool so we can just loop instead to account for eveything.
    for call in [
        mock.call.info('Collecting staticfiles for tenant: %s', tenant='public'),
        mock.call.info(
            '%s files already exist, those uploads will be skipped for tenant: %s', count=2, tenant='public'
        ),
        mock.call.info('Uploading the manifest for tenant: %s', tenant='public'),
        mock.call.info('Collecting staticfiles for tenant: %s', tenant='tenant1'),
        mock.call.info(
            '%s files already exist, those uploads will be skipped for tenant: %s', count=2, tenant='tenant1'
        ),
        mock.call.info('Uploading the manifest for tenant: %s', tenant='tenant1'),
        mock.call.info('Collecting staticfiles for tenant: %s', tenant='tenant2'),
        mock.call.info(
            '%s files already exist, those uploads will be skipped for tenant: %s', count=2, tenant='tenant2'
        ),
        mock.call.info('Uploading the manifest for tenant: %s', tenant='tenant2'),
    ]:
        assert call in mock_logger.mock_calls


@mock.patch.dict(os.environ, {'ENV': 'production'})
@mock.patch('dalme_app.management.commands.collectstatic_tenants.staticfiles_storage')
@mock.patch('dalme_app.management.commands.collectstatic_tenants.call_command')
@mock.patch('dalme_app.management.commands.collectstatic_tenants.Tenant')
@mock.patch('dalme_app.management.commands.collectstatic_tenants.logger')
def test_collectstatic_tenants_exists_force(mock_logger, mock_tenant, mock_call_command, mock_storage):
    tenant_1 = mock.MagicMock(spec=Tenant)
    tenant_1.schema_name = 'tenant1'
    tenant_2 = mock.MagicMock(spec=Tenant)
    tenant_2.schema_name = 'tenant2'
    mock_tenant.objects.all.return_value = [tenant_1, tenant_2]
    mock_storage.exists.return_value = True

    with mock.patch(
        'dalme_app.management.commands.collectstatic_tenants.open_rb', mock.mock_open(read_data=MANIFEST_DATA)
    ) as mock_open:
        CollectstaticTenants().handle(force=True)

        assert mock_open.call_count == 15  # noqa: PLR2004

    assert mock_call_command.called

    # The order is non-deterministic in the following data because of the
    # threading pool so we can just loop instead to account for eveything.
    for call in [
        mock.call.exists('staticfiles.json'),
        mock.call.save('some/css/file.a2194c262648.css', mock_open.return_value),
        mock.call.save('some/js/file.034cc7d8a67f.js', mock_open.return_value),
        mock.call.save('staticfiles.json', mock_open.return_value),
    ]:
        assert call in mock_storage.mock_calls

    for call in [
        mock.call.info('Collecting staticfiles for tenant: %s', tenant='public'),
        mock.call.info('Forcing the reupload of all staticfiles for tenant: %s', tenant='public'),
        mock.call.info('Uploading %s files for tenant: %s', count=2, tenant='public'),
        mock.call.info('File was uploaded to: %s/%s', tenant='public', path='some/js/file.034cc7d8a67f.js'),
        mock.call.info('File was uploaded to: %s/%s', tenant='public', path='some/css/file.a2194c262648.css'),
        mock.call.info('Uploading the manifest for tenant: %s', tenant='public'),
        mock.call.info('Collecting staticfiles for tenant: %s', tenant='tenant1'),
        mock.call.info('Forcing the reupload of all staticfiles for tenant: %s', tenant='tenant1'),
        mock.call.info('Uploading %s files for tenant: %s', count=2, tenant='tenant1'),
        mock.call.info('File was uploaded to: %s/%s', tenant='tenant1', path='some/js/file.034cc7d8a67f.js'),
        mock.call.info('File was uploaded to: %s/%s', tenant='tenant1', path='some/css/file.a2194c262648.css'),
        mock.call.info('Uploading the manifest for tenant: %s', tenant='tenant1'),
        mock.call.info('Collecting staticfiles for tenant: %s', tenant='tenant2'),
        mock.call.info('Forcing the reupload of all staticfiles for tenant: %s', tenant='tenant2'),
        mock.call.info('Uploading %s files for tenant: %s', count=2, tenant='tenant2'),
        mock.call.info('File was uploaded to: %s/%s', tenant='tenant2', path='some/js/file.034cc7d8a67f.js'),
        mock.call.info('File was uploaded to: %s/%s', tenant='tenant2', path='some/css/file.a2194c262648.css'),
        mock.call.info('Uploading the manifest for tenant: %s', tenant='tenant2'),
    ]:
        assert call in mock_logger.mock_calls
