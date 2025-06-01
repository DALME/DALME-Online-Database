"""Define record model factories for the domain app."""

import factory
from faker import Faker

fake = Faker()


class RecordFactory(factory.django.DjangoModelFactory):
    """Factory for creating Record instances."""

    class Meta:
        model = 'domain.Record'

    name = fake.sentence()
    short_name = fake.word()
