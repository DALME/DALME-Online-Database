"""Test the dalme_app.utils.ensure_tenants module."""
import json
import os
from unittest import mock

from dalme_app.management.commands.ensure_tenants import Command as EnsureTenants
from dalme_app.models import Domain, Tenant


@mock.patch.dict(os.environ, {'TENANTS': json.dumps({
    'DALME': {
        'domain': 'dalme.localhost',
        'name': 'DALME',
        'schema_name': 'dalme',
    },
    'GLOBALPHARMACOPEIAS': {
        'domain': 'globalpharmacopeias.localhost',
        'name': 'Global Pharmacopeias',
        'schema_name': 'globalpharmacopeias',
    },
})})
@mock.patch('dalme_app.management.commands.ensure_tenants.Domain')
@mock.patch('dalme_app.management.commands.ensure_tenants.Tenant')
@mock.patch('dalme_app.management.commands.ensure_tenants.logger')
def test_ensure_tenants_exists(mock_logger, mock_tenant, mock_domain):
    mock_tenant.objects.filter.return_value.exists.side_effect = [True, False]
    new_tenant = mock.MagicMock(spec=Tenant)
    new_domain =  mock.MagicMock(spec=Domain)
    mock_tenant.objects.create.return_value = new_tenant
    mock_domain.objects.create.return_value = new_domain

    EnsureTenants().handle()

    assert mock_tenant.mock_calls == [
        mock.call.objects.filter(name='DALME'),
        mock.call.objects.filter().exists(),
        mock.call.objects.filter(name='Global Pharmacopeias'),
        mock.call.objects.filter().exists(),
        mock.call.objects.create(
            name='Global Pharmacopeias',
            schema_name='globalpharmacopeias',
        ),
    ]
    assert mock_domain.mock_calls == [
        mock.call.objects.create(
            domain='globalpharmacopeias.localhost',
            tenant=new_tenant,
            is_primary=False,
        ),
    ]
    assert mock_logger.mock_calls == [
        mock.call.info(
            'Existing tenant %s found for domain: %s',
            tenant='DALME',
            domain='dalme.localhost',
        ),
        mock.call.info('Created tenant', tenant=new_tenant, domain=new_domain),
    ]
