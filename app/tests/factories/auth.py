"""Define model factories for the auth system."""

import factory

from oauth.models import GroupProperties

from .tenant import TenantFactory


class UserFactory(factory.DjangoModelFactory):
    """Generate User model fixtures."""

    class Meta:
        model = 'domain.User'
        django_get_or_create = ('email', 'username')

    username = factory.Sequence(lambda n: 'User %03d' % n)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.Faker('password')
    is_superuser = False
    is_staff = False
    is_active = True

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):  # noqa: ARG002
        """Add objects to the groups m2m relation.

        These should be passed in via the GroupFactory in tests themselves.

        """
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        self.permissions.add(*extracted)


class GroupPropertiesFactory(factory.django.DjangoModelFactory):
    """Generate GroupProperties model fixtures."""

    class Meta:
        model = 'oauth.GroupProperties'

    group_type = factory.fuzzy.FuzzyChoice(GroupProperties.GROUP_TYPES, getter=lambda c: c[0])
    description = factory.Sequence(lambda n: 'Some group description %03d' % n)
    tenant = factory.SubFactory(TenantFactory)


class GroupFactory(factory.django.DjangoModelFactory):
    """Generate Group model fixtures."""

    class Meta:
        model = 'auth.Group'

    name = factory.Sequence(lambda n: 'Group %03d' % n)
    properties = factory.RelatedFactory(GroupPropertiesFactory, factory_related_name='group')

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):  # noqa: ARG002
        """Add objets to the permissions m2m relation.

        These should be passed in via the Permission:w
        Factory in tests themselves.

        """
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        self.permissions.add(*extracted)
