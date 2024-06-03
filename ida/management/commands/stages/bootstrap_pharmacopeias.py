"""Bootstrap pharmacopeias site."""

import os

from django_tenants.utils import schema_context
from wagtail.log_actions import log
from wagtail.rich_text import RichText

from django.db import transaction

from .base import BaseStage

SAMPLE_GRADIENTS = [
    {
        'colour_1': '#064e8c80',
        'colour_2': '#114a2880',
        'angle': '125',
        'description': 'Homepage header',
    },
    {
        'colour_1': '#5386a0b3',
        'colour_2': '#3f6544e6',
        'angle': '125',
        'description': 'Project section headers',
    },
    {
        'colour_1': '#63623ab3',
        'colour_2': '#8a4747e6',
        'angle': '125',
        'description': 'About section headers',
    },
]

DEFAULT_SETTINGS = {
    'name': 'HP',
    'short_form': 'HP',
    'tagline': 'Historical Pharmacopeias',
    'search_tagline': 'Collections of Historical Pharmacopeias',
    'explore_tagline': 'Collections of Historical Pharmacopeias',
    'team_profiles_url': '/about/people/',
}

HOME_DATA = {
    'title': 'Historical Pharmacopeias',
    'slug': 'historical-pharmacopeias',
    'body': [
        (
            'text',
            RichText(
                '<p>Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>'
            ),
        ),
    ],
    'show_in_menus': True,
}

PROJECT_DATA = {'title': 'Project', 'show_in_menus': True}
ABOUT_DATA = {'title': 'About', 'show_in_menus': True}
PROJECT_FLAT_DATA = [
    {
        'title': 'Overview',
        'citable': False,
        'body': [
            (
                'text',
                RichText(
                    '<p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.</p>'
                ),
            ),
        ],
    },
]
ABOUT_FLAT_DATA = [
    {
        'title': 'About HP',
        'body': [
            (
                'text',
                RichText(
                    '<p>Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.</p>'
                ),
            ),
        ],
        'show_contact_form': True,
    },
]


class Stage(BaseStage):
    """Bootstraps pharmacopeias site."""

    name = '13 Bootstrapping pharmacopeias public site'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        with schema_context('pharmacopeias'):
            from wagtail.models import Page

            from public.models import Home

            if (env := os.environ.get('ENV')) == 'production':
                self.logger.info('This command should never be run in production')
            elif env == 'staging' and Home.objects.exists():
                self.logger.warning('Skipping site generation as the CMS tree already exists')
            else:
                self.create_gradient_records()
                self.create_default_settings()
                self.home = self.create_home()
                self.create_project_section()
                self.create_about_section()

                for page in Page.objects.all():
                    if not page.is_root():
                        page.specific.save_revision().publish()

                self.logger.info('Created Pharmacopeias site!')

    @transaction.atomic
    def create_gradient_records(self):
        """Create records for some sample gradients."""
        self.logger.info('Adding gradients to PHARMACOPEIAS tenant')
        with schema_context('pharmacopeias'):
            from public.extensions.gradients.models import Gradient

            for entry in SAMPLE_GRADIENTS:
                gradient_obj = Gradient.objects.create(**entry)
                log(instance=gradient_obj, action='wagtail.create')

    @transaction.atomic
    def create_default_settings(self):
        """Create default settings and preferences."""
        self.logger.info('Creating default settings')
        with schema_context('pharmacopeias'):
            from public.models import Settings

            Settings.objects.create(**DEFAULT_SETTINGS)

    def create_about_section(self):
        """Create about section."""
        self.logger.info('Creating "About" section')
        with schema_context('pharmacopeias'):
            from public.models import Flat, Section

            section = self.home.add_child(instance=Section(**ABOUT_DATA))
            for flat_data in ABOUT_FLAT_DATA:
                section.add_child(instance=Flat(**flat_data))

    def create_project_section(self):
        """Create project section."""
        self.logger.info('Creating "Project" section')
        with schema_context('pharmacopeias'):
            from public.models import Flat, Section

            section = self.home.add_child(instance=Section(**PROJECT_DATA))
            for flat_data in PROJECT_FLAT_DATA:
                section.add_child(instance=Flat(**flat_data))

    def create_home(self):
        """Create homepage."""
        self.logger.info('Creating homepage')
        with schema_context('pharmacopeias'):
            from wagtail.models import Page, Site

            from public.models import Home

            try:
                Site.objects.first().delete()
                Page.objects.last().delete()
            except AttributeError:
                pass

            root = Page.objects.first()
            home = root.add_child(instance=Home(**HOME_DATA))

            Site.objects.create(
                hostname='localhost',
                site_name='Historical Pharmacopeias',
                root_page=home,
                is_default_site=True,
            )
            return home
