"""Test the app.management.commands.ensure_tenants module."""

from unittest import mock

import pytest

from django.conf import settings

from app.settings import TenantTypes
from tenants.management.commands.ensure_tenants import Command as EnsureTenants
from tenants.models import Domain, Tenant


@pytest.mark.django_db
@mock.patch('tenants.management.commands.ensure_tenants.Domain')
@mock.patch('tenants.management.commands.ensure_tenants.Tenant')
@mock.patch('tenants.management.commands.ensure_tenants.logger')
def test_ensure_tenants_existence(mock_logger, mock_tenant, mock_domain):
    new_tenant = mock.MagicMock(spec=Tenant)
    new_domain = mock.MagicMock(spec=Domain)
    mock_tenant.objects.create.return_value = new_tenant
    mock_domain.objects.create.return_value = new_domain

    mock_qs = mock.MagicMock()

    mock_ida_tenant = mock.MagicMock(spec=Tenant)
    mock_ida_domain = mock.MagicMock(spec=Domain)
    mock_ida_domain.domain = settings.TENANTS().IDA.value.domain
    mock_ida_tenant.domains.first.return_value = mock_ida_domain
    for attr, value in settings.TENANTS().IDA.value.__dict__.items():
        setattr(mock_ida_tenant, attr, value)

    mock_dalme_tenant = mock.MagicMock(spec=Tenant)
    mock_dalme_domain = mock.MagicMock(spec=Domain)
    mock_dalme_domain.domain = settings.TENANTS().DALME.value.domain
    mock_dalme_tenant.domains.first.return_value = mock_dalme_domain
    for attr, value in settings.TENANTS().DALME.value.__dict__.items():
        setattr(mock_dalme_tenant, attr, value)

    mock_tenant.objects.filter.return_value = mock_qs
    mock_qs.exists.side_effect = [True, True, False]
    mock_qs.first.side_effect = [mock_ida_tenant, mock_dalme_tenant]

    EnsureTenants().handle()

    assert mock_tenant.mock_calls == [
        mock.call.objects.filter(name='IDA'),
        mock.call.objects.filter().exists(),
        mock.call.objects.filter().first(),
        mock.call.objects.filter(name='DALME'),
        mock.call.objects.filter().exists(),
        mock.call.objects.filter().first(),
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


@pytest.mark.django_db
@mock.patch('tenants.management.commands.ensure_tenants.Domain')
@mock.patch('tenants.management.commands.ensure_tenants.Tenant')
@mock.patch('tenants.management.commands.ensure_tenants.logger')
def test_ensure_tenants_name_updates_error(mock_logger, mock_tenant, mock_domain):
    new_tenant = mock.MagicMock(spec=Tenant)
    new_domain = mock.MagicMock(spec=Domain)
    mock_tenant.objects.create.return_value = new_tenant
    mock_domain.objects.create.return_value = new_domain

    mock_qs = mock.MagicMock()

    mock_ida_tenant = mock.MagicMock(spec=Tenant)
    mock_ida_domain = mock.MagicMock(spec=Domain)
    mock_ida_domain.domain = settings.TENANTS().IDA.value.domain
    mock_ida_tenant.domains.first.return_value = mock_ida_domain
    for attr, value in settings.TENANTS().IDA.value.__dict__.items():
        setattr(mock_ida_tenant, attr, value)
        mock_ida_tenant.name = 'Forbidden'

    mock_dalme_tenant = mock.MagicMock(spec=Tenant)
    mock_dalme_domain = mock.MagicMock(spec=Domain)
    mock_dalme_domain.domain = settings.TENANTS().DALME.value.domain
    mock_dalme_tenant.domains.first.return_value = mock_dalme_domain
    for attr, value in settings.TENANTS().DALME.value.__dict__.items():
        setattr(mock_dalme_tenant, attr, value)

    mock_tenant.objects.filter.return_value = mock_qs
    mock_qs.exists.side_effect = [True, True, False]
    mock_qs.first.side_effect = [mock_ida_tenant, mock_dalme_tenant]

    with pytest.raises(ValueError) as exc:  # noqa: PT011
        EnsureTenants().handle()

    assert str(exc.value) == "Don't mutate existing tenant names, they should be write-once/immutable."

    assert mock_tenant.mock_calls == [
        mock.call.objects.filter(name='IDA'),
        mock.call.objects.filter().exists(),
        mock.call.objects.filter().first(),
    ]
    assert not mock_domain.mock_calls

    assert mock_logger.mock_calls == [
        mock.call.info(
            'Existing tenant found for domain',
            tenant='IDA',
            domain='ida.localhost',
        ),
    ]


@pytest.mark.django_db
@mock.patch('tenants.management.commands.ensure_tenants.Domain')
@mock.patch('tenants.management.commands.ensure_tenants.Tenant')
@mock.patch('tenants.management.commands.ensure_tenants.logger')
def test_ensure_tenants_schema_name_updates_error(mock_logger, mock_tenant, mock_domain):
    new_tenant = mock.MagicMock(spec=Tenant)
    new_domain = mock.MagicMock(spec=Domain)
    mock_tenant.objects.create.return_value = new_tenant
    mock_domain.objects.create.return_value = new_domain

    mock_qs = mock.MagicMock()

    mock_ida_tenant = mock.MagicMock(spec=Tenant)
    mock_ida_domain = mock.MagicMock(spec=Domain)
    mock_ida_domain.domain = settings.TENANTS().IDA.value.domain
    mock_ida_tenant.domains.first.return_value = mock_ida_domain
    for attr, value in settings.TENANTS().IDA.value.__dict__.items():
        setattr(mock_ida_tenant, attr, value)
        mock_ida_tenant.schema_name = 'Forbidden'

    mock_dalme_tenant = mock.MagicMock(spec=Tenant)
    mock_dalme_domain = mock.MagicMock(spec=Domain)
    mock_dalme_domain.domain = settings.TENANTS().DALME.value.domain
    mock_dalme_tenant.domains.first.return_value = mock_dalme_domain
    for attr, value in settings.TENANTS().DALME.value.__dict__.items():
        setattr(mock_dalme_tenant, attr, value)

    mock_tenant.objects.filter.return_value = mock_qs
    mock_qs.exists.side_effect = [True, True, False]
    mock_qs.first.side_effect = [mock_ida_tenant, mock_dalme_tenant]

    with pytest.raises(ValueError) as exc:  # noqa: PT011
        EnsureTenants().handle()

    assert str(exc.value) == "Don't mutate existing tenant schema names, they should be write-once/immutable."

    assert mock_tenant.mock_calls == [
        mock.call.objects.filter(name='IDA'),
        mock.call.objects.filter().exists(),
        mock.call.objects.filter().first(),
    ]
    assert not mock_domain.mock_calls

    assert mock_logger.mock_calls == [
        mock.call.info(
            'Existing tenant found for domain',
            tenant='IDA',
            domain='ida.localhost',
        ),
    ]


@pytest.mark.django_db
@mock.patch('tenants.management.commands.ensure_tenants.Domain')
@mock.patch('tenants.management.commands.ensure_tenants.Tenant')
@mock.patch('tenants.management.commands.ensure_tenants.logger')
def test_ensure_tenants_tenant_type_updates_error(mock_logger, mock_tenant, mock_domain):
    new_tenant = mock.MagicMock(spec=Tenant)
    new_domain = mock.MagicMock(spec=Domain)
    mock_tenant.objects.create.return_value = new_tenant
    mock_domain.objects.create.return_value = new_domain

    mock_qs = mock.MagicMock()

    mock_ida_tenant = mock.MagicMock(spec=Tenant)
    mock_ida_domain = mock.MagicMock(spec=Domain)
    mock_ida_domain.domain = settings.TENANTS().IDA.value.domain
    mock_ida_tenant.domains.first.return_value = mock_ida_domain
    for attr, value in settings.TENANTS().IDA.value.__dict__.items():
        setattr(mock_ida_tenant, attr, value)
        mock_ida_tenant.tenant_type = TenantTypes.PROJECT

    mock_dalme_tenant = mock.MagicMock(spec=Tenant)
    mock_dalme_domain = mock.MagicMock(spec=Domain)
    mock_dalme_domain.domain = settings.TENANTS().DALME.value.domain
    mock_dalme_tenant.domains.first.return_value = mock_dalme_domain
    for attr, value in settings.TENANTS().DALME.value.__dict__.items():
        setattr(mock_dalme_tenant, attr, value)

    mock_tenant.objects.filter.return_value = mock_qs
    mock_qs.exists.side_effect = [True, True, False]
    mock_qs.first.side_effect = [mock_ida_tenant, mock_dalme_tenant]

    with pytest.raises(ValueError) as exc:  # noqa: PT011
        EnsureTenants().handle()

    assert str(exc.value) == "Don't mutate existing tenant types, they should be write-once/immutable."

    assert mock_tenant.mock_calls == [
        mock.call.objects.filter(name='IDA'),
        mock.call.objects.filter().exists(),
        mock.call.objects.filter().first(),
    ]
    assert not mock_domain.mock_calls

    assert mock_logger.mock_calls == [
        mock.call.info(
            'Existing tenant found for domain',
            tenant='IDA',
            domain='ida.localhost',
        ),
    ]


@pytest.mark.django_db
@mock.patch('tenants.management.commands.ensure_tenants.Domain')
@mock.patch('tenants.management.commands.ensure_tenants.Tenant')
@mock.patch('tenants.management.commands.ensure_tenants.logger')
def test_ensure_tenants_domain_updates(mock_logger, mock_tenant, mock_domain):
    new_tenant = mock.MagicMock(spec=Tenant)
    new_domain = mock.MagicMock(spec=Domain)
    mock_tenant.objects.create.return_value = new_tenant
    mock_domain.objects.create.return_value = new_domain

    mock_qs = mock.MagicMock()

    mock_ida_tenant = mock.MagicMock(spec=Tenant)
    mock_ida_domain = mock.MagicMock(spec=Domain)
    mock_ida_domain.domain = 'foobar.com'
    mock_ida_tenant.domains.first.return_value = mock_ida_domain
    for attr, value in settings.TENANTS().IDA.value.__dict__.items():
        setattr(mock_ida_tenant, attr, value)

    mock_dalme_tenant = mock.MagicMock(spec=Tenant)
    mock_dalme_domain = mock.MagicMock(spec=Domain)
    mock_dalme_domain.domain = 'bazquux.com'
    mock_dalme_tenant.domains.first.return_value = mock_dalme_domain
    for attr, value in settings.TENANTS().DALME.value.__dict__.items():
        setattr(mock_dalme_tenant, attr, value)

    mock_tenant.objects.filter.return_value = mock_qs
    mock_qs.exists.side_effect = [True, True, False]
    mock_qs.first.side_effect = [mock_ida_tenant, mock_dalme_tenant]

    EnsureTenants().handle()

    assert mock_tenant.mock_calls == [
        mock.call.objects.filter(name='IDA'),
        mock.call.objects.filter().exists(),
        mock.call.objects.filter().first(),
        mock.call.objects.filter(name='DALME'),
        mock.call.objects.filter().exists(),
        mock.call.objects.filter().first(),
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
        mock.call.info('Updated tenant domain record.', tenant='IDA', domain='ida.localhost'),
        mock.call.info(
            'Existing tenant found for domain',
            tenant='DALME',
            domain='dalme.localhost',
        ),
        mock.call.info('Updated tenant domain record.', tenant='DALME', domain='dalme.localhost'),
        mock.call.info('Tenant created', tenant=new_tenant, domain=new_domain),
    ]
