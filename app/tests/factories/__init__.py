"""Interface for the tests.factories module."""

from tests.factories.app import OwnedModelFactory, TrackedModelFactory, UUIDModelFactory
from tests.factories.domain import OrganizationFactory, PersonFactory
from tests.factories.oauth import GroupFactory, GroupPropertiesFactory, UserFactory
from tests.factories.web import TeamMemberFactory, TeamMemberRoleFactory


class ResourceFactory:
    """Resource factory factory.

    The name of the resource is pluralized to preserve the symmetry with the
    RESTful name of the resource, which is also plural, eg.

    `/api/oauth/users/`
    `/api/domain/agents/people/`
    `/api/tenant/organizations/`

    """

    FACTORIES = {
        'organizations': OrganizationFactory,
        'people': PersonFactory,
        'user_groups': GroupFactory,
        'user_group_properties': GroupPropertiesFactory,
        'users': UserFactory,
        'team_members': TeamMemberFactory,
        'team_member_roles': TeamMemberRoleFactory,
        'owned_models': OwnedModelFactory,
        'uuid_models': UUIDModelFactory,
        'tracked_models': TrackedModelFactory,
    }

    def __init__(self):
        """Initialize a `ResourceFactory` instance."""
        for resource, factory in self.FACTORIES.items():
            setattr(self, resource, factory)


__all__ = [
    'ResourceFactory',
]
