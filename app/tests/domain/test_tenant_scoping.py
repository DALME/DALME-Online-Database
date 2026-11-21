"""Test that tenanted data stays with the tenant it belongs to."""

from unittest import mock

import pytest
from rest_framework.request import Request

from django.db import connection
from django.db.models import QuerySet

from domain.models import OptionsValue, Record, TaskList
from domain.signals import wagtail_index_post_delete_signal_handler, wagtail_index_post_save_signal_handler

from tests.factories.fakers import fake


def evaluate_queryset(viewset_class, arf):
    view = viewset_class()
    view.request = Request(arf.get('/'))
    view.action = 'list'
    return view.get_queryset()


@pytest.mark.django_db
def test_no_viewset_holds_a_tenanted_queryset_from_class_definition(current_tenant):  # noqa: ARG001
    from domain.api.router import router

    frozen = [
        prefix
        for prefix, viewset, _basename in router.registry
        if isinstance(getattr(viewset, 'queryset', None), QuerySet)
        and getattr(viewset.queryset.model, 'is_tenanted', False)
    ]

    assert frozen == []


@pytest.mark.django_db
def test_tenanted_viewset_scopes_to_the_tenant_bound_when_evaluated(
    as_tenant, test_tenant, other_tenant, arf, factories
):
    with as_tenant(test_tenant):
        from domain.api.resources.tasks.endpoints import TaskLists

        factories.task_lists.create(tenant=test_tenant)

    with as_tenant(other_tenant):
        expected = factories.task_lists.create(tenant=other_tenant)

        found = list(evaluate_queryset(TaskLists, arf))

    assert found == [expected]


@pytest.mark.django_db
def test_a_saved_row_keeps_the_tenant_it_was_saved_under(as_tenant, test_tenant, other_tenant):
    with as_tenant(test_tenant):
        # Saved without a tenant, so `TenantMixin.save` fills it in from the context.
        task_list = TaskList.objects.create(name=fake.sentence(nb_words=3)[:60])

    with as_tenant(other_tenant):
        assert task_list.tenant.pk == test_tenant.pk

    assert task_list.tenant.pk == test_tenant.pk


@pytest.mark.django_db
def test_creating_a_row_that_names_its_tenant_needs_none_bound(test_tenant, factories):
    op_list = factories.options_lists.create()

    value = OptionsValue.objects.create(op_list=op_list, payload=fake.words(nb=2), tenant=test_tenant)
    task_list = TaskList.objects.create(name=fake.sentence(nb_words=3)[:60], tenant=test_tenant)

    assert (value.tenant.pk, task_list.tenant.pk) == (test_tenant.pk, test_tenant.pk)


@pytest.mark.django_db
def test_creating_a_row_without_a_tenant_needs_one_bound():
    with pytest.raises(RuntimeError, match='not bound'):
        TaskList.objects.create(name=fake.sentence(nb_words=3)[:60])


@pytest.mark.django_db
def test_an_untenanted_option_lookup_returns_only_the_lists_own_values(test_tenant, other_tenant, factories):
    factories.options_values.create(tenant=test_tenant)
    own_list = factories.options_lists.create()
    payload = fake.words(nb=3)
    own_values = {
        factories.options_values.create(op_list=own_list, payload=payload, tenant=tenant)
        for tenant in (test_tenant, other_tenant)
    }

    assert set(own_list.values.unscoped()) == own_values
    assert own_list.get_values(tenanted=False, raw_data=True) == payload


@pytest.mark.django_db
@pytest.mark.parametrize(
    ('handler', 'index_call'),
    [
        (wagtail_index_post_save_signal_handler, 'insert_or_update_object'),
        (wagtail_index_post_delete_signal_handler, 'remove_object'),
    ],
)
def test_record_index_signals_restore_the_schema(handler, index_call, test_tenant, other_tenant):
    indexed_in = []
    connection.set_tenant(test_tenant)
    try:
        with mock.patch('domain.signals.index') as index:
            getattr(index, index_call).side_effect = lambda _instance: indexed_in.append(connection.schema_name)
            handler(instance=Record())
        schema_after = connection.schema_name
    finally:
        connection.set_schema_to_public()

    assert schema_after == test_tenant.schema_name
    assert sorted(indexed_in) == sorted([test_tenant.schema_name, other_tenant.schema_name])
