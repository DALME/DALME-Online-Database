"""Run s3manifestcollectstatic for all db schemas.

Adapted from: https://github.com/dduong42/s3manifestcollectstatic

"""
import json
import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from tempfile import TemporaryDirectory

import structlog
from django_tenants.utils import tenant_context

from django.contrib.staticfiles.management.commands import collectstatic
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage, staticfiles_storage
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from dalme_app.models import Tenant

logger = structlog.get_logger(__name__)


MANIFEST_PATH = 'staticfiles.json'


class Command(BaseCommand):
    """Define the collectstatic_tenants command."""

    help = 'Collect staticfiles for all registered tenants.'  # noqa: A003

    @property
    def is_dev(self):
        """Are we running in dev mode or not."""
        return os.environ['ENV'] in {'development', 'ci'}

    def add_arguments(self, parser):
        """Configure accepted managment command arguments."""
        parser.add_argument(
            '-f',
            '--force',
            action='store_true',
            help='Force the reupload of files',
        )
        parser.add_argument(
            '-w',
            '--max-workers',
            type=int,
            help='Max number of workers',
        )

    def collectstatic(self, *args):  # noqa: ARG002
        """Invoke the normal django collectstatic command."""
        command = collectstatic.Command()
        call_command(command)

    def collectstatic_s3(self, tenant, options):
        """Efficiently upload staticfiles to s3."""
        with tenant_context(tenant):
            self.force = options.get('force', False)
            self.max_workers = options.get('max_workers')

            if self.max_workers is not None and self.max_workers <= 0:
                msg = 'The maximum number of workers must be greater than 0.'
                raise CommandError(msg)

            with TemporaryDirectory() as tmpdirname:
                command = collectstatic.Command()
                command.storage = ManifestStaticFilesStorage(location=tmpdirname)
                call_command(command)

                manifest = Path(tmpdirname) / MANIFEST_PATH
                with manifest.open('rb') as f:
                    to_upload = set(json.load(f)['paths'].values())

                if staticfiles_storage.exists(MANIFEST_PATH):
                    with staticfiles_storage.open(MANIFEST_PATH) as f:
                        already_uploaded = set(json.load(f)['paths'].values())
                        intersection = to_upload.intersection(already_uploaded)
                        logger.info('%s files were already uploaded', len(intersection))

                        if self.force:
                            logger.info('Forcing the reupload of files')
                        else:
                            to_upload.difference_update(already_uploaded)

                def _save_asset(path):
                    path_obj = Path(tmpdirname) / path
                    with path_obj.open('rb') as f, tenant_context(tenant):
                        staticfiles_storage.save(path, f)
                    return path

                logger.info('Start the upload of %s files', len(to_upload))
                with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                    for path in executor.map(_save_asset, to_upload):
                        logger.info('Path was uploaded: %s', path)

                logger.info('Uploading the manifest')
                _save_asset(MANIFEST_PATH)

    def handle(self, *args, **options):  # noqa: ARG002
        """Collect staticfiles."""
        command = self.collectstatic if self.is_dev else self.collectstatic_s3
        connection.set_schema_to_public()
        logger.info('Collecting staticfiles for: public')
        command(connection.tenant, options)

        for tenant in Tenant.objects.all():
            logger.info('Collecting staticfiles for: %s', tenant)
            command(tenant, options)
