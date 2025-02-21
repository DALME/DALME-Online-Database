"""Customize staticfiles storage logic."""

import structlog
from storages.backends.s3boto3 import S3Boto3Storage, S3ManifestStaticStorage

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import connection

from app.context import get_current_tenant

logger = structlog.get_logger(__name__)


class StorageOverride(S3ManifestStaticStorage):
    """Debug me."""

    def read_manifest(self):
        try:
            with self.manifest_storage.open(self.manifest_name) as manifest:
                return manifest.read().decode()
        except FileNotFoundError:
            logger.exception(self.location)
            raise


class StaticStorage(S3ManifestStaticStorage):
    """Multitenant aware staticfiles storage class for S3."""

    key = 'static'

    def __init__(self, *args, **kwargs):
        location = f'{settings.AWS_STORAGE_BUCKET_NAME}/{self.location}'
        manifest_storage = StorageOverride(location=location)
        super().__init__(*args, manifest_storage=manifest_storage, **kwargs)

    @property
    def schema(self):
        """Get the tenant schema name."""
        try:
            return get_current_tenant().schema_name
        except RuntimeError:
            return connection.tenant.schema_name

    @property
    def location(self):
        """Get the schema qualified filepath."""
        return f'{self.key}/{self.schema}'


class MediaStorage(S3Boto3Storage):
    """Multitenant aware media files storage class for S3."""

    file_overwrite = False
    key = 'media'

    @property
    def schema(self):
        """Get the tenant schema name."""
        try:
            return get_current_tenant().schema_name
        except RuntimeError:
            return connection.tenant.schema_name

    @property
    def location(self):
        """Get the schema qualified filepath."""
        return f'{self.key}/{self.schema}'


class LocalMediaStorage(FileSystemStorage):
    """Multitenant aware media files storage class for local filesystem."""

    @property
    def base_url(self):
        return f'{settings.MEDIA_URL}/{self.schema}/'

    @property
    def schema(self):
        """Get the tenant schema name."""
        try:
            return get_current_tenant().schema_name
        except RuntimeError:
            return connection.tenant.schema_name

    @property
    def location(self):
        """Get the schema qualified filepath."""
        return f'{settings.MEDIA_ROOT}/{self.schema}'
