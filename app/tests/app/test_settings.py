"""Tests for the settings module."""

import json
import os
from unittest import mock

import app.settings as settings_mod


def test_tenanttypes_enum():
    assert settings_mod.TenantTypes.PUBLIC == 'public'
    assert settings_mod.TenantTypes.PROJECT == 'project'


def test_tenant_dataclass_iter():
    t = settings_mod.TENANT(
        domain='d',
        name='n',
        schema_name='s',
        is_primary=True,
        tenant_type=settings_mod.TenantTypes.PUBLIC,
    )
    values = tuple(t)
    assert values == ('d', 'n', 's', True, settings_mod.TenantTypes.PUBLIC)


def test_base_templates_property():
    dev = settings_mod.Development()
    templates = dev.TEMPLATES
    assert isinstance(templates, list)
    assert templates[0]['BACKEND'] == 'django.template.backends.django.DjangoTemplates'


def test_base_multitenant_staticfiles_dirs():
    dev = settings_mod.Development()
    dirs = dev.MULTITENANT_STATICFILES_DIRS
    assert isinstance(dirs, list)
    assert '%s/static' in dirs[0]


def test_base_tenants_pristinemethod():
    dev = settings_mod.Development()
    tenants_enum = dev.TENANTS()
    assert hasattr(tenants_enum, 'IDA')
    assert hasattr(tenants_enum, 'DALME')
    assert hasattr(tenants_enum, 'PHARMACOPEIAS')
    assert tenants_enum.IDA.value.domain == 'ida.localhost'


def test_base_tenants_env_override():
    tenants_dict = {
        'FOO': {
            'domain': 'foo.localhost',
            'name': 'Foo',
            'schema_name': 'foo',
            'is_primary': True,
            'tenant_type': 'public',
        }
    }
    with mock.patch.dict(os.environ, {'TENANTS': json.dumps(tenants_dict)}):
        dev = settings_mod.Development()
        tenants_enum = dev.TENANTS()
        assert hasattr(tenants_enum, 'FOO')
        assert tenants_enum.FOO.value.domain == 'foo.localhost'


def test_development_installed_apps():
    dev = settings_mod.Development()
    apps = dev.INSTALLED_APPS()
    assert 'django_tenants' in apps
    assert 'django_extensions' in apps
    assert 'web' in apps


def test_development_database_properties():
    with mock.patch.dict(
        os.environ,
        {
            'POSTGRES_DB': 'testdb',
            'POSTGRES_USER': 'testuser',
            'POSTGRES_PASSWORD': 'testpass',
            'POSTGRES_HOST': 'testhost',
            'POSTGRES_PORT': '5433',
        },
    ):
        dev = settings_mod.Development()
        assert dev.POSTGRES_DB == 'testdb'
        assert dev.POSTGRES_USER == 'testuser'
        assert dev.POSTGRES_PASSWORD == 'testpass'
        assert dev.POSTGRES_HOST == 'testhost'
        assert dev.POSTGRES_PORT == 5433  # noqa: PLR2004


def test_development_database_defaults():
    with mock.patch.dict(os.environ, {}, clear=True):
        # Ensure defaults are set correctly
        dev = settings_mod.Development()
        assert dev.POSTGRES_DB == 'ida'
        assert dev.POSTGRES_USER == 'ida'
        assert dev.POSTGRES_PASSWORD == 'ida'
        assert dev.POSTGRES_HOST == 'localhost'
        assert dev.POSTGRES_PORT == 5432  # noqa: PLR2004


def test_development_dam_db_properties():
    with mock.patch.dict(
        os.environ,
        {
            'DAM_DB_NAME': 'damdb',
            'DAM_DB_USER': 'damuser',
            'DAM_DB_PASSWORD': 'dampass',
            'DAM_DB_HOST': 'damhost',
            'DAM_DB_PORT': '3307',
        },
    ):
        dev = settings_mod.Development()
        assert dev.DAM_DB_NAME == 'damdb'
        assert dev.DAM_DB_USER == 'damuser'
        assert dev.DAM_DB_PASSWORD == 'dampass'
        assert dev.DAM_DB_HOST == 'damhost'
        assert dev.DAM_DB_PORT == 3307  # noqa: PLR2004


def test_development_dam_db_defaults():
    with mock.patch.dict(os.environ, {}, clear=True):
        dev = settings_mod.Development()
        assert dev.DAM_DB_NAME == 'dam'
        assert dev.DAM_DB_USER == 'dam'
        assert dev.DAM_DB_PASSWORD == 'dam'
        assert dev.DAM_DB_HOST == 'localhost'
        assert dev.DAM_DB_PORT == 3306  # noqa: PLR2004


def test_development_databases():
    dev = settings_mod.Development()
    dbs = dev.DATABASES
    assert 'default' in dbs
    assert 'dam' in dbs
    assert dbs['default']['ENGINE'] == 'django_tenants.postgresql_backend'
    assert dbs['dam']['ENGINE'] == 'django.db.backends.mysql'


def test_test_storages():
    test_settings = settings_mod.Test()
    storages = test_settings.STORAGES
    assert storages['default']['BACKEND'] == 'tenants.storage_backends.MemoryMediaStorage'
    assert storages['staticfiles']['BACKEND'] == 'tenants.storage_backends.MemoryStaticStorage'
    assert storages['avatars']['BACKEND'] == 'django.core.files.storage.memory.InMemoryStorage'


def test_production_properties():
    with mock.patch.dict(
        os.environ,
        {
            'DOMAIN': 'dalme.org',
            'ALLOWED_HOSTS': '["dalme.org", "api.dalme.org"]',
            'AWS_STORAGE_BUCKET_NAME': 'bucket',
            'ELASTICSEARCH_ENDPOINT': 'es.dalme.org',
            'ELASTICSEARCH_USER': 'esuser',
            'ELASTICSEARCH_PASSWORD': 'espass',
            'TENANT_DOMAINS': '["dalme.org", "api.dalme.org"]',
            'DJANGO_SECRET_KEY': 'prodsecret',
        },
    ):
        prod = settings_mod.Production()
        assert prod.BASE_URL == 'dalme.org'
        assert prod.ALLOWED_HOSTS == ['dalme.org', 'api.dalme.org']
        assert prod.AWS_STORAGE_BUCKET_NAME == 'bucket'
        assert prod.AWS_S3_CUSTOM_DOMAIN == 'dalme.org'
        assert prod.MEDIA_URL.startswith('https://dalme.org/')
        assert prod.STATIC_URL.startswith('https://dalme.org/')
        assert prod.TENANT_DOMAINS == ['dalme.org', 'api.dalme.org']
        assert prod.SECRET_KEY == 'prodsecret'


def test_production_elasticsearch_dsl():
    with mock.patch.dict(
        os.environ,
        {
            'ELASTICSEARCH_ENDPOINT': 'es.dalme.org',
            'ELASTICSEARCH_USER': 'esuser',
            'ELASTICSEARCH_PASSWORD': 'espass',
        },
    ):
        prod = settings_mod.Production()
        es = prod.ELASTICSEARCH_DSL
        assert es['default']['host'] == 'es.dalme.org'
        assert es['default']['port'] == 443  # noqa: PLR2004
        assert es['default']['http_auth'] == ('esuser', 'espass')
        assert es['default']['use_ssl'] is True
        assert es['default']['verify_certs'] is True


def test_production_oauth2_provider():
    with mock.patch.dict(os.environ, {'OIDC_RSA_PRIVATE_KEY': 'PRIVATEKEY'}):
        prod = settings_mod.Production()
        # OAUTH2_SCOPES is a dict, so just check keys
        oauth2 = prod.OAUTH2_PROVIDER
        assert oauth2['OIDC_RSA_PRIVATE_KEY'] == 'PRIVATEKEY'
        assert 'SCOPES' in oauth2


def test_staging_tenants():
    staging = settings_mod.Staging()
    tenants = staging._TENANTS  # noqa: SLF001
    assert 'IDA' in tenants
    assert tenants['IDA']['domain'] == 'documentaryarchaeology.net'
    assert tenants['DALME']['schema_name'] == 'dalme'
    assert tenants['PHARMACOPEIAS']['tenant_type'] == settings_mod.TenantTypes.PROJECT
