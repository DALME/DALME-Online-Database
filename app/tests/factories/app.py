"""Define model factories for the app app."""

import factory
from faker import Faker


def _generate_initialism(name):
    """Return the initials of the passed name."""
    return ''.join([i.upper() for i in name.split()])


class AbstractFactory(factory.django.DjangoModelFactory):
    """Generate a generic model fixture."""

    class Meta:
        app_label = 'abstract'

    @factory.lazy_attribute
    def name(self):
        """Randomly generate an English name."""
        fake = Faker(['en_US'])
        return fake.name()
