"""Define record model factories for the domain app."""

import factory

from tests.factories.fakers import fake


class RecordFactory(factory.django.DjangoModelFactory):
    """Generate record fixtures titled in the corpus's patterns."""

    class Meta:
        model = 'domain.Record'

    name = factory.LazyFunction(fake.record_title)
    short_name = factory.LazyFunction(fake.archival_reference)
