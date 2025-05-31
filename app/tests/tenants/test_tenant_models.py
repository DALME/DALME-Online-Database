"""Tests for Tenant and Domain models."""

import pytest
from django_tenants.utils import get_tenant_type_choices


@pytest.mark.django_db
def test_tenant_creation(factories):
    tenant = factories.tenants.create(name='TestTenant', schema_name='test_tenant')
    assert tenant.name == 'TestTenant'
    assert tenant.tenant_type == 'project'
    assert tenant.schema_name == 'test_tenant'
    assert tenant.id is not None


# @pytest.mark.django_db
# def test_tenant_unique_name_constraint(factories):
#     factories.tenants.create(name='UniqueTenant', schema_name='unique_tenant')
#     # with pytest.raises(Exception):
#     factories.tenants.create(name='UniqueTenant', schema_name='unique_tenant')


# @pytest.mark.django_db
# def test_tenant_members_relationship(factories):
#     user1 = factories.users.create(username='user1')
#     user2 = factories.users.create(username='user2')
#     tenant = factories.tenants.create(name='MembersTenant', schema_name='members_tenant')
#     tenant.members.add(user1, user2)
#     assert tenant.members.count() == 2
#     assert user1 in tenant.members.all()
#     assert user2 in tenant.members.all()


@pytest.mark.django_db
def test_tenant_type_choices_and_default(factories):
    choices = [choice[0] for choice in get_tenant_type_choices()]
    tenant = factories.tenants.create(name='TypeTenant', schema_name='type_tenant')
    assert tenant.tenant_type in choices
    assert tenant.tenant_type == 'project'


@pytest.mark.django_db
def test_domain_creation(factories, test_tenant):
    domain = factories.domains.create(tenant=test_tenant)
    assert domain.pk is not None
