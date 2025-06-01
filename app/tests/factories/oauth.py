"""Define model factories for the auth system."""

import factory
from factory import fuzzy

from oauth.models import GroupProperties
from tenants.models import Tenant


class UserFactory(factory.django.DjangoModelFactory):
    """Generate User model fixtures."""

    class Meta:
        model = 'oauth.User'
        django_get_or_create = ('username',)
        skip_postgeneration_save = True

    class Params:
        staff = factory.Trait(is_staff=True)
        superuser = factory.Trait(is_staff=True, is_superuser=True)

    username = factory.Sequence(lambda n: 'User%03d' % n)  # noqa: UP031
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.django.Password('password')
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

        self.groups.add(*extracted)


class GroupPropertiesFactory(factory.django.DjangoModelFactory):
    """Generate GroupProperties model fixtures."""

    class Meta:
        model = 'oauth.GroupProperties'

    group_type = fuzzy.FuzzyChoice(GroupProperties.GROUP_TYPES, getter=lambda c: c[0])
    description = factory.Sequence(lambda n: 'Some group description %03d' % n)  # noqa: UP031
    tenant = factory.Iterator(Tenant.objects.all())


class GroupFactory(factory.django.DjangoModelFactory):
    """Generate Group model fixtures."""

    class Meta:
        model = 'auth.Group'
        skip_postgeneration_save = True

    name = factory.Sequence(lambda n: 'Group %03d' % n)  # noqa: UP031
    properties = factory.RelatedFactory(GroupPropertiesFactory, factory_related_name='group')

    @factory.post_generation
    def permissions(self, create, extracted, **kwargs):  # noqa: ARG002
        """Add objects to the permissions m2m relation.

        These should be passed in via the Permission Factory in tests themselves.

        """
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        self.permissions.add(*extracted)
