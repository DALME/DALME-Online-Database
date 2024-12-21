"""Define model factories for the Tenant model."""

import factory


class DomainFactory(factory.django.DjangoModelFactory):
    """Generate Domain model fixtures."""

    domain = factory.Sequence(lambda n: 'Domain %03d' % n)
    is_primary = False  # We don't use a primary domain.

    class Meta:
        model = 'tenants.Domain'


class TenantFactory(factory.django.DjangoModelFactory):
    """Generate Tenant model fixtures."""

    class Meta:
        model = 'tenants.Tenant'

    name = factory.Sequence(lambda n: 'Tenant %03d' % n)
    domains = factory.RelatedFactory(DomainFactory, factory_related_name='tenant')

    @factory.post_generation
    def members(self, create, extracted, **kwargs):  # noqa: ARG002
        """Add objects to the members m2m relation.

        These should be passed in via the UserFactory in tests themselves.

        """
        if not create or not extracted:
            # Simple build, or nothing to add, do nothing.
            return

        self.members.add(*extracted)
