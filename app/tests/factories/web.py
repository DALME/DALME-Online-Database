"""Define model factories for the web app."""

from datetime import UTC

import factory
from faker import Faker as TheRealFaker
from wagtail.models import Site
from wagtail_factories import PageFactory

from web.models import BasePage, FeaturedPage

from .domain import RecordFactory
from .oauth import UserFactory

fake = TheRealFaker()


# --- Snippet/utility models ---
class SponsorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'web.Sponsor'

    name = factory.Faker('company')
    logo = None
    url = factory.Faker('url')


class SocialMediaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'web.SocialMedia'

    name = factory.Faker('word')
    icon = factory.Faker('word')
    css_class = factory.Faker('word')
    url = factory.Faker('url')


class FooterLinkFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'web.FooterLink'

    label = factory.Faker('word')
    page = None


# --- Wagtail settings ---
class SettingsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'web.Settings'

    name = factory.Faker('company')
    short_form = factory.Faker('word')
    tagline = factory.Faker('sentence')
    logo = factory.Faker('file_path')
    copyright_line = factory.Faker('sentence')
    analytics_domain = factory.Faker('domain_name')
    contact_email = factory.Faker('email')
    team_profiles_url = factory.Faker('uri_path')
    publication_title = factory.Faker('sentence')
    publication_url = factory.Faker('url')
    doi_handle = factory.Faker('word')


# --- Page models ---
class BasePageFactory(PageFactory):
    class Meta:
        model = BasePage
        abstract = True

    title = factory.Faker('sentence')
    header_position = 'top'
    live = True
    slug = factory.Faker('slug')
    go_live_at = factory.Faker('date_time_this_decade', before_now=True, after_now=False, tzinfo=UTC)
    last_published_at = factory.LazyAttribute(
        lambda x: fake.date_time_between(start_date=x.go_live_at, end_date='now', tzinfo=UTC)
    )


class HomeFactory(BasePageFactory):
    class Meta:
        model = 'web.Home'

    short_title = 'Home'
    slug = 'home-page'
    # learn_more_page = None


class SectionFactory(BasePageFactory):
    class Meta:
        model = 'web.Section'

    short_title = factory.Faker('word')
    title = factory.Faker('word')


class FeaturesFactory(BasePageFactory):
    class Meta:
        model = 'web.Features'


class FlatFactory(BasePageFactory):
    class Meta:
        model = 'web.Flat'

    short_title = factory.Faker('word')


class BibliographyFactory(BasePageFactory):
    class Meta:
        model = 'web.Bibliography'

    short_title = factory.Faker('word')


class PeopleFactory(BasePageFactory):
    class Meta:
        model = 'web.People'


class CollectionsFactory(BasePageFactory):
    class Meta:
        model = 'web.Collections'


class CollectionFactory(BasePageFactory):
    class Meta:
        model = 'web.Collection'


class FeaturedPageFactory(BasePageFactory):
    class Meta:
        model = FeaturedPage
        abstract = True

    owner = factory.SubFactory(UserFactory)


class FeaturedObjectFactory(FeaturedPageFactory):
    class Meta:
        model = 'web.FeaturedObject'

    record = factory.SubFactory(RecordFactory)


class FeaturedInventoryFactory(FeaturedPageFactory):
    class Meta:
        model = 'web.FeaturedInventory'

    record = factory.SubFactory(RecordFactory)


class EssayFactory(FeaturedPageFactory):
    class Meta:
        model = 'web.Essay'


# --- Site model ---
class SiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Site

    hostname = factory.Faker('domain_name')
    port = factory.Sequence(lambda n: 81 + n)
    site_name = 'Test site'
    root_page = factory.SubFactory(HomeFactory, parent=None)
    is_default_site = False
