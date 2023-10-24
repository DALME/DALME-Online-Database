"""Customize staticfiles storage logic."""
from django_tenants.utils import parse_tenant_config_path
from storages.backends.s3boto3 import S3ManifestStaticStorage

from django.contrib.staticfiles.storage import ManifestStaticFilesStorage


class LocalStorage(ManifestStaticFilesStorage):
    """Local file system storage with S3 read fallbacks for development."""


class StaticStorage(S3ManifestStaticStorage):
    """Multitenant aware staticfiles storage class for S3."""

    default_acl = None
    file_overwrite = False
    custom_domain = False

    def get_default_settings(self):
        settings = super().get_default_settings()
        settings['location'] = parse_tenant_config_path('%s')
        return settings


class MediaStorage(S3ManifestStaticStorage):
    """Multitenant aware media files storage class for S3."""

    default_acl = None
    file_overwrite = False
    custom_domain = False

    def get_default_settings(self):
        settings = super().get_default_settings()
        settings['location'] = f'media/{parse_tenant_config_path("%s")}'
        return settings
