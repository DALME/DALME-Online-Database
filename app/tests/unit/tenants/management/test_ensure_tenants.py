"""Test the app.management.commands.ensure_tenants module."""

from unittest import mock

import pytest

from django.db import DataError

from app.settings import TenantTypes
from tenants.management.commands.ensure_tenants import Command as EnsureTenants
from tenants.models import Domain, Tenant


@mock.patch('tenants.management.commands.ensure_tenants.Domain')
@mock.patch('tenants.management.commands.ensure_tenants.Tenant')
@mock.patch('tenants.management.commands.ensure_tenants.logger')
def test_ensure_tenants_exists_mismatch(mock_logger, mock_tenant, mock_domain):
    mock_tenant.objects.filter.return_value.exists.side_effect = [True, False]

    with pytest.raises(DataError):
        EnsureTenants().handle()

    assert mock_tenant.mock_calls == [
        mock.call.objects.filter(name='IDA'),
        mock.call.objects.filter().exists(),
        mock.call.objects.filter(domains__domain='ida.localhost'),
        mock.call.objects.filter().exists(),
    ]
    assert mock_domain.called is False
    assert mock_logger.mock_calls == [
        mock.call.error(
            'Invalid existing tenant record for this environment',
            tenant='IDA',
            domain='ida.localhost',
        ),
    ]


@mock.patch('tenants.management.commands.ensure_tenants.Domain')
@mock.patch('tenants.management.commands.ensure_tenants.Tenant')
@mock.patch('tenants.management.commands.ensure_tenants.logger')
def test_ensure_tenants_exists(mock_logger, mock_tenant, mock_domain):
    mock_tenant.objects.filter.return_value.exists.side_effect = [True, True, True, True, False]
    new_tenant = mock.MagicMock(spec=Tenant)
    new_domain = mock.MagicMock(spec=Domain)
    mock_tenant.objects.create.return_value = new_tenant
    mock_domain.objects.create.return_value = new_domain

    EnsureTenants().handle()

    assert mock_tenant.mock_calls == [
        mock.call.objects.filter(name='IDA'),
        mock.call.objects.filter().exists(),
        mock.call.objects.filter(domains__domain='ida.localhost'),
        mock.call.objects.filter().exists(),
        mock.call.objects.filter(name='DALME'),
        mock.call.objects.filter().exists(),
        mock.call.objects.filter(domains__domain='dalme.localhost'),
        mock.call.objects.filter().exists(),
        mock.call.objects.filter(name='Pharmacopeias'),
        mock.call.objects.filter().exists(),
        mock.call.objects.create(
            name='Pharmacopeias',
            schema_name='pharmacopeias',
            tenant_type=TenantTypes.PROJECT.value,
        ),
    ]
    assert mock_domain.mock_calls == [
        mock.call.objects.create(
            domain='pharmacopeias.localhost',
            tenant=new_tenant,
            is_primary=False,
        ),
    ]
    assert mock_logger.mock_calls == [
        mock.call.info(
            'Existing tenant found for domain',
            tenant='IDA',
            domain='ida.localhost',
        ),
        mock.call.info(
            'Existing tenant found for domain',
            tenant='DALME',
            domain='dalme.localhost',
        ),
        mock.call.info('Tenant created', tenant=new_tenant, domain=new_domain),
    ]
