"""Customize staticfiles storage logic."""
from django_tenants.utils import parse_tenant_config_path
from storages.backends.s3boto3 import S3Boto3Storage, S3ManifestStaticStorage


class StaticStorage(S3ManifestStaticStorage):
    """Multitenant aware staticfiles storage class for S3."""

    default_acl = None
    file_overwrite = False

    @property
    def location(self):
        return 'static/%s'

    def get_default_settings(self):
        settings = super().get_default_settings()
        settings['location'] = parse_tenant_config_path('static/%s')
        return settings


class MediaStorage(S3Boto3Storage):
    """Multitenant aware media files storage class for S3."""

    default_acl = None

    @property
    def location(self):
        return 'media/%s'

    def get_default_settings(self):
        settings = super().get_default_settings()
        settings['location'] = parse_tenant_config_path('media/%s')
        return settings
