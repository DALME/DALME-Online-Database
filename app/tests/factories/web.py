"""Define model factories for the web app."""

import factory

from web.models import FeaturedPage

from .oauth import UserFactory


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
class HomeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'web.Home'

    title = factory.Faker('sentence')
    short_title = factory.Faker('word')
    header_position = 'top'
    # learn_more_page = None


class SectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'web.Section'

    title = factory.Faker('sentence')
    short_title = factory.Faker('word')
    header_position = 'top'


class FeaturesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'web.Features'

    title = factory.Faker('sentence')
    short_title = factory.Faker('word')
    header_position = 'top'


class FlatFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'web.Flat'

    title = factory.Faker('sentence')
    short_title = factory.Faker('word')
    header_position = 'top'
    show_contact_form = False


class BibliographyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'web.Bibliography'

    title = factory.Faker('sentence')
    short_title = factory.Faker('word')
    header_position = 'top'


class PeopleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'web.People'

    title = factory.Faker('sentence')
    short_title = factory.Faker('word')
    header_position = 'top'


class CollectionsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'web.Collections'

    title = factory.Faker('sentence')
    short_title = factory.Faker('word')
    header_position = 'top'


class CollectionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'web.Collection'

    title = factory.Faker('sentence')
    short_title = factory.Faker('word')
    header_position = 'top'
    # record_collection = None


class FeaturedPageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FeaturedPage
        abstract = True

    title = factory.Faker('sentence')
    header_position = 'top'
    live = True
    owner = factory.SubFactory(UserFactory)
    last_published_at = factory.Faker('date_time_this_decade', before_now=True, after_now=False)
    path = '000100010002000R'
    depth = 4


class FeaturedObjectFactory(FeaturedPageFactory):
    class Meta:
        model = 'web.FeaturedObject'


class FeaturedInventoryFactory(FeaturedPageFactory):
    class Meta:
        model = 'web.FeaturedInventory'


class EssayFactory(FeaturedPageFactory):
    class Meta:
        model = 'web.Essay'
