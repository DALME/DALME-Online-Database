"""Define agent model factories for the domain app."""

import factory

from tests.factories.fakers import fake


def _generate_initialism(name):
    """Return the initials of the passed name."""
    return ''.join([i.upper() for i in name.split()])


class OrganizationFactory(factory.django.DjangoModelFactory):
    """Generate organization fixtures."""

    class Meta:
        model = 'domain.Organization'

    short_name = factory.LazyAttribute(lambda x: _generate_initialism(x.name))

    name = factory.LazyFunction(fake.company)


class PersonFactory(factory.django.DjangoModelFactory):
    """Generate person fixtures.

    This factory is for generating **Bare Agent** person` instances. That is to
    say, `Person` records that have no related `User`.

    """

    class Meta:
        model = 'domain.Person'

    class Params:
        bare_agent = factory.Trait(user=None)

    user = None
    name = factory.LazyFunction(fake.historical_name)
