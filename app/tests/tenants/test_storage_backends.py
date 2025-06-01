"""Tests for tenant storage backends."""

from unittest import mock

import pytest
from moto import mock_aws

from django.conf import settings

from tenants import storage_backends


@pytest.fixture
def mock_parse_tenant_config_path():
    with mock.patch('tenants.storage_backends.parse_tenant_config_path') as m:
        m.side_effect = lambda s: f'parsed/{s}'
        yield m


def test_tenant_storage_mixin_get_default_settings(mock_parse_tenant_config_path):  # noqa: ARG001
    class Parent:
        def get_default_settings(self):
            return {'foo': 'bar'}

    class TestStorage(storage_backends.TenantStorageMixin, Parent):
        key = 'static'

    s = TestStorage()
    settings = s.get_default_settings()
    assert settings['foo'] == 'bar'
    assert settings['location'] == 'parsed/static/%s'


def test_tenant_storage_mixin_get_location(mock_parse_tenant_config_path):  # noqa: ARG001
    class TestStorage(storage_backends.TenantStorageMixin):
        key = 'media'

    s = TestStorage()
    loc = s._get_location()  # noqa: SLF001
    assert loc == 'parsed/media/%s'


@mock_aws
def test_s3staticstorage_remap_manifest_changes_location(mock_parse_tenant_config_path):  # noqa: ARG001
    s = storage_backends.S3StaticStorage()
    s.location = 'old/location'
    s._get_location = mock.Mock(return_value='new/location')  # noqa: SLF001
    s.load_manifest = mock.Mock(return_value=({'foo': 'bar'}, 'hash'))
    with mock.patch('tenants.storage_backends.S3ManifestStaticStorage') as mock_manifest:
        s._remap_manifest()  # noqa: SLF001
        assert s.location == 'new/location'
        mock_manifest.assert_called_with(location='new/location')
        assert s.hashed_files == {'foo': 'bar'}
        assert s.manifest_hash == 'hash'


@mock_aws
def test_s3staticstorage_remap_manifest_no_change(mock_parse_tenant_config_path):  # noqa: ARG001
    s = storage_backends.S3StaticStorage()
    s.location = 'same/location'
    s._get_location = mock.Mock(return_value='same/location')  # noqa: SLF001
    s.load_manifest = mock.Mock()
    with mock.patch('tenants.storage_backends.S3ManifestStaticStorage') as mock_manifest:
        s._remap_manifest()  # noqa: SLF001
        mock_manifest.assert_not_called()
        s.load_manifest.assert_not_called()


@mock_aws
def test_s3mediastorage_remap_location_changes(mock_parse_tenant_config_path):  # noqa: ARG001
    s = storage_backends.S3MediaStorage()
    s.location = 'old/location'
    s._get_location = mock.Mock(return_value='new/location')  # noqa: SLF001
    s._remap_location()  # noqa: SLF001
    assert s.location == 'new/location'


@mock_aws
def test_s3mediastorage_remap_location_no_change(mock_parse_tenant_config_path):  # noqa: ARG001
    s = storage_backends.S3MediaStorage()
    s.location = 'same/location'
    s._get_location = mock.Mock(return_value='same/location')  # noqa: SLF001
    s._remap_location()  # noqa: SLF001
    assert s.location == 'same/location'


def test_localstaticstorage_base_location_and_url(mock_parse_tenant_config_path):  # noqa: ARG001
    class TestStorage(storage_backends.LocalStaticStorage):
        key = 'static'
        _location = None
        _base_url = None

    s = TestStorage()
    assert s.base_location == f'parsed/{settings.STATIC_ROOT}/%s'
    assert s.base_url == settings.STATIC_URL


def test_localmediastorage_base_location_and_url(mock_parse_tenant_config_path):  # noqa: ARG001
    class TestStorage(storage_backends.LocalMediaStorage):
        key = 'media'
        _location = None
        _base_url = None

    s = TestStorage()
    assert s.base_location == f'parsed/{settings.MEDIA_ROOT}/%s'
    assert s.base_url == f'parsed/{settings.MEDIA_URL}/%s'


def test_localmediastorage_key():
    s = storage_backends.LocalMediaStorage()
    assert s.key == 'media'


def test_localstaticstorage_key():
    s = storage_backends.LocalStaticStorage()
    assert s.key == 'static'
