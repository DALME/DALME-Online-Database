"""Customize staticfiles storage logic."""

import structlog
from django_tenants.utils import parse_tenant_config_path
from storages.backends.s3 import S3ManifestStaticStorage, S3Storage

from django.conf import settings
from django.core.files.storage import FileSystemStorage, InMemoryStorage

logger = structlog.get_logger(__name__)


def safe_parse_tenant_config_path(key):
    """Ensure this helper function cannot throw.

    This can happen at startup when the model definitions need to
    know about settings.STORAGES but the Django app hasn't booted up
    in full meaning the schema has not been set on the connection
    yet. In which case, just initialize it to the default schema.

    """
    try:
        return parse_tenant_config_path(f'{key}/%s')
    except AttributeError:
        return f'{key}/public'


class TenantStorageMixin:
    """Reusable multitenant storage functionality."""

    def get_default_settings(self):
        settings = super().get_default_settings()
        settings['location'] = self._get_location()
        return settings

    def _get_location(self):
        return safe_parse_tenant_config_path(self.key)


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


class S3MediaStorage(TenantStorageMixin, S3Storage):
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

    key_dict = {
        'media': {
            'root': 'MEDIA_ROOT',
            'url': 'MEDIA_URL',
        },
        'static': {
            'root': 'STATIC_ROOT',
            'url': 'STATIC_URL',
        },
    }

    @property
    def base_location(self):
        """Get the schema qualified filepath."""
        key = getattr(settings, self.key_dict[self.key]['root'])
        return safe_parse_tenant_config_path(key)

    @property
    def base_url(self):
        key = getattr(settings, self.key_dict[self.key]['url'])
        if self.key == 'static':
            return key
        return safe_parse_tenant_config_path(key)


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
