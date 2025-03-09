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
    """Reusable multitenant storage functionality."""

    def get_default_settings(self):
        settings = super().get_default_settings()
        settings['location'] = self._get_location()
        return settings

    def _get_location(self):
        return parse_tenant_config_path(f'{self.key}/%s')


class StaticStorage(TenantStorageMixin, S3ManifestStaticStorage):
    """Multitenant aware staticfiles storage class for S3.

    We have to make sure to recompute the manifest data whenever the tenant
    search path changes because otherwise the manifest is only parsed and read
    once at application startup time when it will just be pointing to 'public'
    because it is outside any request/response cycle.

    """

    key = 'static'

    def _normalize_name(self, name):
        self._remap_manifest()
        return super()._normalize_name(name)

    def _remap_manifest(self):
        if (location := self._get_location()) != self.location:
            self.location = location
            self.manifest_storage = S3ManifestStaticStorage(location=location)
            self.hashed_files, self.manifest_hash = self.load_manifest()


class MediaStorage(TenantStorageMixin, S3Boto3Storage):
    """Multitenant aware media files storage class for S3."""

    file_overwrite = False
    key = 'media'

    def _normalize_name(self, name):
        self._remap_location()
        return super()._normalize_name(name)

    def _remap_location(self):
        if (location := self._get_location()) != self.location:
            self.location = location


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
