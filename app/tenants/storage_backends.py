"""Customize staticfiles storage logic."""

import structlog
from django_tenants.utils import parse_tenant_config_path
from storages.backends.s3boto3 import S3Boto3Storage, S3ManifestStaticStorage

from django.core.files.storage import FileSystemStorage, InMemoryStorage

logger = structlog.get_logger(__name__)


class TenantStorageMixin:
    """Reusable multitenant storage functionality."""

    def get_default_settings(self):
        settings = super().get_default_settings()
        settings['location'] = self._get_location()
        return settings

    def _get_location(self):
        return parse_tenant_config_path(f'{self.key}/%s')


class S3StaticStorage(TenantStorageMixin, S3ManifestStaticStorage):
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


class S3MediaStorage(TenantStorageMixin, S3Boto3Storage):
    """Multitenant aware media files storage class for S3."""

    file_overwrite = False
    key = 'media'

    def _normalize_name(self, name):
        self._remap_location()
        return super()._normalize_name(name)

    def _remap_location(self):
        if (location := self._get_location()) != self.location:
            self.location = location


class LocalTenantStorageMixin:
    """Reusable local multitenant storage functionality."""

    @property
    def base_location(self):
        return self._value_or_setting(self._location, parse_tenant_config_path(f'{self.key}/%s'))

    @property
    def base_url(self):
        if self._base_url is not None and not self._base_url.endswith('/'):
            self._base_url += '/'
        return self._value_or_setting(self._base_url, parse_tenant_config_path(f'{self.key}/%s'))


class LocalMediaStorage(LocalTenantStorageMixin, FileSystemStorage):
    """Multitenant aware media files storage class for local filesystem."""

    key = 'media'


class MemoryMediaStorage(LocalTenantStorageMixin, InMemoryStorage):
    """Multitenant aware media files storage class for in-memory storage (for use during tests)."""

    key = 'media'


class LocalStaticStorage(LocalTenantStorageMixin, FileSystemStorage):
    """Multitenant aware static file storage class for local filesystem."""

    key = 'static'


class MemoryStaticStorage(LocalTenantStorageMixin, InMemoryStorage):
    """Multitenant aware static file storage class for in-memory storage (for use during tests)."""

    key = 'static'
