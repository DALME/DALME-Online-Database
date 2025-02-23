"""Customize staticfiles storage logic."""

import structlog
from django_tenants.utils import parse_tenant_config_path
from storages.backends.s3boto3 import S3Boto3Storage, S3ManifestStaticStorage

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import connection

from app.context import get_current_tenant

logger = structlog.get_logger(__name__)


class TenantStorageMixin:
    """Reusable mutltitenant storage functionality."""

    def get_default_settings(self):
        settings = super().get_default_settings()
        settings['location'] = self._get_location()
        return settings

    def _get_location(self):
        return parse_tenant_config_path(f'{self.key}/%s')


class StaticStorage(TenantStorageMixin, S3ManifestStaticStorage):
    """Multitenant aware staticfiles storage class for S3."""

    key = 'static'

    # Overrides for strict tenanting over multiple manifests.
    def read_manifest(self):
        with self.manifest_storage.open(self.manifest_name) as manifest:
            data = manifest.read().decode()
            logger.critical('-------- %s/%s --------', self.location, self.manifest_name)
            logger.critical(data)
            return data

    def save_manifest(self):
        self._remap_manifest()
        super().save_manifest()

    def stored_name(self, name):
        self._remap_manifest()
        return super().stored_name(name)

    def _remap_manifest(self):
        if (location := self._get_location()) != self.location:
            self.location = location
            self.manifest_storage = S3ManifestStaticStorage(location=location)
            self.hashed_files, self.manifest_hash = self.load_manifest()


class MediaStorage(TenantStorageMixin, S3Boto3Storage):
    """Multitenant aware media files storage class for S3."""

    file_overwrite = False
    key = 'media'


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
