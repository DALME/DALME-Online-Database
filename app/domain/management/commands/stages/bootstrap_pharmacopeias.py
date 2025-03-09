"""Bootstrap pharmacopeias site."""

import os

from django_tenants.utils import schema_context
from wagtail.log_actions import log

from django.db import transaction

from .base import BaseStage
from .fixtures import (
    ABOUT_DATA,
    ABOUT_FLAT_DATA,
    DEFAULT_SETTINGS,
    HOME_DATA,
    PROJECT_DATA,
    PROJECT_FLAT_DATA,
    SAMPLE_GRADIENTS,
)


class Stage(BaseStage):
    """Bootstraps pharmacopeias site."""

    name = '14 Bootstrapping pharmacopeias public site'

    @transaction.atomic
    def apply(self):
        """Execute the stage."""
        with schema_context('pharmacopeias'):
            from wagtail.models import Page

            from web.models import Home

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
            from web.extensions.gradients.models import Gradient

            for entry in SAMPLE_GRADIENTS:
                gradient_obj = Gradient.objects.create(**entry)
                log(instance=gradient_obj, action='wagtail.create')

    @transaction.atomic
    def create_default_settings(self):
        """Create default settings and preferences."""
        self.logger.info('Creating default settings')
        with schema_context('pharmacopeias'):
            from web.models import Settings

            Settings.objects.create(**DEFAULT_SETTINGS)

    def create_about_section(self):
        """Create about section."""
        self.logger.info('Creating "About" section')
        with schema_context('pharmacopeias'):
            from web.models import Flat, Section

            section = self.home.add_child(instance=Section(**ABOUT_DATA))
            for flat_data in ABOUT_FLAT_DATA:
                section.add_child(instance=Flat(**flat_data))

    def create_project_section(self):
        """Create project section."""
        self.logger.info('Creating "Project" section')
        with schema_context('pharmacopeias'):
            from web.models import Flat, Section

            section = self.home.add_child(instance=Section(**PROJECT_DATA))
            for flat_data in PROJECT_FLAT_DATA:
                section.add_child(instance=Flat(**flat_data))

    def create_home(self):
        """Create homepage."""
        self.logger.info('Creating homepage')
        with schema_context('pharmacopeias'):
            from wagtail.models import Page, Site

            from web.models import Home

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
