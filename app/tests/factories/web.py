"""Define model factories for the web app."""

import factory

from .oauth import UserFactory


class TeamMemberRoleFactory(factory.django.DjangoModelFactory):
    """Generate TeamMember role model fixtures."""

    class Meta:
        model = 'webteam.TeamRole'

    role = factory.Faker('word')
    description = factory.Faker('sentence')
    parent = None


class TeamMemberFactory(factory.django.DjangoModelFactory):
    """Generate TeamMember model fixtures."""

    class Meta:
        model = 'webteam.TeamMember'
        skip_postgeneration_save = True

    user = factory.SubFactory(UserFactory)
    name = factory.Faker('name')
    roles = factory.RelatedFactory(TeamMemberRoleFactory)
    title = factory.Faker('job')
    affiliation = factory.Faker('company')
    biography = factory.Faker('paragraph')
    url = factory.Faker('url')
