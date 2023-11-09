"""Customize staticfiles storage logic."""
from django_tenants.utils import parse_tenant_config_path
from storages.backends.s3boto3 import S3Boto3Storage, S3ManifestStaticStorage
from storages.utils import safe_join

from django.core.exceptions import SuspiciousOperation

from dalme_app.tenant import get_current_tenant


class StaticStorage(S3ManifestStaticStorage):
    """Multitenant aware staticfiles storage class for S3."""

    def _normalize_name(self, name):
        """Override to achieve the schema partitioning we need."""
        try:
            schema = get_current_tenant().schema_name
        except RuntimeError:
            schema = 'public'

        try:
            return safe_join(f'static/{schema}', name)
        except ValueError as exc:
            raise SuspiciousOperation('Attempted access to "%s" denied.' % name) from exc

    def get_default_settings(self):
        settings = super().get_default_settings()
        settings['location'] = parse_tenant_config_path('static/%s')
        return settings


class MediaStorage(S3Boto3Storage):
    """Multitenant aware media files storage class for S3."""

    def _normalize_name(self, name):
        """Override to achieve the schema partitioning we need."""
        try:
            schema = get_current_tenant().schema_name
        except RuntimeError:
            schema = 'public'

        try:
            return safe_join(f'media/{schema}', name)
        except ValueError as exc:
            raise SuspiciousOperation('Attempted access to "%s" denied.' % name) from exc

    def get_default_settings(self):
        settings = super().get_default_settings()
        settings['location'] = parse_tenant_config_path('media/%s')
        return settings
