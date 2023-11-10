"""Run collectstatic for all db schemas.

Adapted from: https://github.com/dduong42/s3manifestcollectstatic

"""
import functools
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

    @staticmethod
    def save_asset(path, tmpdir, tenant):
        """Upload the file data to the bucket.

        We have to set the tenant context here again as we are running inside
        the thread pool. If we don't the tenant will always be 'public' as the
        db connection will not yet have been set within the new thread.

        """
        path_obj = Path(tmpdir) / path
        with tenant_context(tenant), path_obj.open('rb') as f:
            staticfiles_storage.save(path, f)
        return path

    @staticmethod
    def parse_manifest(handle):
        """Read the contents of a static manifest file."""
        return set(json.load(handle)['paths'].values())

    @staticmethod
    def collect(tmpdir):
        """Collect files into a temporary directory and generate a manifest."""
        command = collectstatic.Command()
        command.storage = ManifestStaticFilesStorage(location=tmpdir)
        call_command(command)

    def get_file_data(self, tenant):
        """Process the files and collect the resulting file data for the run."""
        with TemporaryDirectory() as tmpdir:
            self.collect(tmpdir)

            manifest = Path(tmpdir) / MANIFEST_PATH
            with manifest.open('rb') as f:
                to_upload = self.parse_manifest(f)

            # Compare the newly generated manifest with the remote manifest (if
            # it exists) to determine what needs to be sent down the wire.
            if staticfiles_storage.exists(MANIFEST_PATH):
                with staticfiles_storage.open(MANIFEST_PATH) as f:
                    already_uploaded = self.parse_manifest(f)
                    intersection = to_upload.intersection(already_uploaded)

                    if self.force:
                        logger.info(
                            'Forcing the reupload of all staticfiles for tenant: %s',
                            tenant=tenant.schema_name,
                        )
                    else:
                        to_upload.difference_update(already_uploaded)
                        logger.info(
                            '%s files already exist, those uploads will be skipped for tenant: %s',
                            count=len(intersection),
                            tenant=tenant.schema_name,
                        )

            return tmpdir, to_upload

    def collectstatic_s3(self, tenant):
        """Efficiently upload staticfiles to s3."""
        with tenant_context(tenant):
            if self.max_workers is not None and self.max_workers < 1:
                msg = 'The maximum number of workers must be greater than 0.'
                raise CommandError(msg)

            tmpdir, to_upload = self.get_file_data(tenant)
            if (count := len(to_upload)) > 0:
                logger.info('Uploading %s files for tenant: %s', count=count, tenant=tenant.schema_name)

            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                func = functools.partial(self.save_asset, tenant=tenant, tmpdir=tmpdir)
                for path in executor.map(func, to_upload):
                    logger.info('File was uploaded to: %s/%s', tenant=tenant.schema_name, path=path)

            logger.info('Uploading the manifest for tenant: %s', tenant=tenant.schema_name)
            self.save_asset(MANIFEST_PATH, tmpdir, tenant)

    def collectstatic(self, tenant):
        """Invoke the normal django collectstatic command."""
        with tenant_context(tenant):
            call_command(collectstatic.Command())

    def handle(self, *args, **options):  # noqa: ARG002
        """Collect application staticfiles per tenant."""
        self.force = options.get('force', False)
        self.max_workers = options.get('max_workers')

        command = self.collectstatic if self.is_dev else self.collectstatic_s3
        connection.set_schema_to_public()
        logger.info('Collecting staticfiles for tenant: %s', tenant='public')
        command(connection.tenant)

        for tenant in Tenant.objects.all():
            logger.info('Collecting staticfiles for tenant: %s', tenant=tenant.schema_name)
            command(tenant)

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
