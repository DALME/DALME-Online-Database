"""Interface for the tests.factories module."""

from tests.factories.app import OwnedModelFactory, TenantedModelFactory, TrackedModelFactory, UUIDModelFactory
from tests.factories.domain import OrganizationFactory, PersonFactory
from tests.factories.oauth import GroupFactory, GroupPropertiesFactory, UserFactory
from tests.factories.tenants import DomainModelFactory, TenantModelFactory
from tests.factories.web import (
    BibliographyFactory,
    CollectionFactory,
    CollectionsFactory,
    EssayFactory,
    FeaturedInventoryFactory,
    FeaturedObjectFactory,
    FeaturedPageFactory,
    FeaturesFactory,
    FlatFactory,
    FooterLinkFactory,
    HomeFactory,
    PeopleFactory,
    SectionFactory,
    SettingsFactory,
    SiteFactory,
    SocialMediaFactory,
    SponsorFactory,
)
from tests.factories.web_team import TeamMemberFactory, TeamMemberRoleFactory


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
        'tenanted_models': TenantedModelFactory,
        'tenants': TenantModelFactory,
        'domains': DomainModelFactory,
        'essay_pages': EssayFactory,
        'collection_pages': CollectionFactory,
        'collections_pages': CollectionsFactory,
        'features_pages': FeaturesFactory,
        'featured_object_pages': FeaturedObjectFactory,
        'featured_pages': FeaturedPageFactory,
        'featured_inventory_pages': FeaturedInventoryFactory,
        'bibliography_pages': BibliographyFactory,
        'flat_pages': FlatFactory,
        'pages_sections': SectionFactory,
        'settings_pages': SettingsFactory,
        'social_media_snippets': SocialMediaFactory,
        'sponsor_snippets': SponsorFactory,
        'home_pages': HomeFactory,
        'footer_links_snippets': FooterLinkFactory,
        'people_pages': PeopleFactory,
        'sites': SiteFactory,
    }

    def __init__(self):
        """Initialize a `ResourceFactory` instance."""
        for resource, factory in self.FACTORIES.items():
            setattr(self, resource, factory)


__all__ = [
    'ResourceFactory',
]
