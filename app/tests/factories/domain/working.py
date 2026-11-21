"""Define factories for each project's own working material.

These models carry a tenant. A factory takes the tenant bound for the test (the
`current_tenant` fixture), or an explicit `tenant=`.

"""

import factory

from app.context import get_current_tenant

from tests.factories.fakers import fake


def bound_tenant():
    """Return the tenant bound for the test, or explain how to provide one."""
    try:
        return get_current_tenant()._get_current_object()  # noqa: SLF001
    except RuntimeError as exc:
        msg = 'Bind a tenant (the `current_tenant` fixture) or pass `tenant=` to a tenanted factory.'
        raise RuntimeError(msg) from exc


class TenantedFactory(factory.django.DjangoModelFactory):
    """Give a tenanted model the bound tenant unless one is passed."""

    class Meta:
        abstract = True

    tenant = factory.LazyFunction(bound_tenant)


class TaskListFactory(TenantedFactory):
    """Generate task list fixtures."""

    class Meta:
        model = 'domain.TaskList'

    name = factory.LazyFunction(lambda: fake.sentence(nb_words=3)[:60])


class TaskFactory(TenantedFactory):
    """Generate task fixtures, each in a list of the same tenant."""

    class Meta:
        model = 'domain.Task'

    title = factory.LazyFunction(lambda: fake.sentence(nb_words=6)[:140])
    description = factory.LazyFunction(fake.paragraph)
    task_list = factory.SubFactory(TaskListFactory, tenant=factory.SelfAttribute('..tenant'))


class DomainCollectionFactory(TenantedFactory):
    """Generate collection fixtures: a project's sets of records."""

    class Meta:
        model = 'domain.Collection'

    name = factory.LazyFunction(lambda: fake.sentence(nb_words=4))


class OptionsListFactory(factory.django.DjangoModelFactory):
    """Generate options list fixtures. Lists are shared; their values are not."""

    class Meta:
        model = 'domain.OptionsList'

    name = factory.LazyFunction(lambda: fake.sentence(nb_words=3))
    payload_type = 'static_list'
    description = factory.LazyFunction(fake.sentence)


class OptionsValueFactory(TenantedFactory):
    """Generate one tenant's values for an options list."""

    class Meta:
        model = 'domain.OptionsValue'

    op_list = factory.SubFactory(OptionsListFactory)
    payload = factory.LazyFunction(lambda: fake.words(nb=3))


class PreferenceKeyFactory(factory.django.DjangoModelFactory):
    """Generate preference key fixtures. Every user gets a preference for each key."""

    class Meta:
        model = 'domain.PreferenceKey'

    name = factory.Sequence(lambda n: f'{fake.word()}{n}')
    label = factory.LazyFunction(lambda: fake.sentence(nb_words=2))
    description = factory.LazyFunction(fake.sentence)
    data_type = 'STR'
    group = factory.LazyFunction(fake.word)
    default = factory.LazyFunction(fake.word)
