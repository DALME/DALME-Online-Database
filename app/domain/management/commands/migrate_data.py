"""Management command to migrate DALME data to the new schema.

Care should be taken to make each stage atomic, idempotent and immutable, so we
are able to maintain complete control and transparency during this procedure
(qualities that were lacking with our previous Django migrations attempt).

"""

import structlog

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from .stages import (
    AttributeOptionsStage,
    AttributesStage,
    AttributeTypesStage,
    AuthStage,
    CollectionsStage,
    ContentFixes,
    EntitiesStage,
    FinalizeStage,
    PharmaStage,
    PublicStage,
    RankOneStage,
    RankTwoStage,
    RankZeroStage,
    RecordsStage,
    TeiElements,
)

logger = structlog.get_logger(__name__)

STAGES = [
    AuthStage,
    RankZeroStage,
    RankOneStage,
    RankTwoStage,
    AttributeTypesStage,
    AttributeOptionsStage,
    AttributesStage,
    RecordsStage,
    FinalizeStage,
    CollectionsStage,
    PublicStage,
    ContentFixes,
    PharmaStage,
    TeiElements,
    EntitiesStage,
]


class Command(BaseCommand):
    """Define the migrate_data command."""

    def migrate(self):
        """Run the migration pipeline."""
        try:
            assert settings.ZOTERO_API_KEY
            assert settings.ZOTERO_API_KEY_GP
            assert settings.ZOTERO_LIBRARY_ID
            assert settings.ZOTERO_LIBRARY_ID_GP

        except AssertionError:
            logger.exception('Zotero environment variables are not set')
            raise

        for cls in STAGES:
            stage = cls()
            label = f'Applying migration stage: {stage.name}'
            separator = '-' * (len(label) + 2)
            logger.info(separator)
            logger.info(label)
            logger.info(separator)
            stage.apply()

    def handle(self, *args, **options):  # noqa: ARG002
        """Migrate DALME data."""
        if not settings.IS_DEV:
            err = 'This command should not be run outside of a development environment'
            raise CommandError(err, returncode=1)

        logger.info('Initializing data migration')
        call_command('ensure_tenants')
        logger.info('All tenants exist. Proceeding')

        self.migrate()

        logger.info('Data migration complete')
