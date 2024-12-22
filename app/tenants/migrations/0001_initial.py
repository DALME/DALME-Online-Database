# Generated by Django 5.0.4 on 2024-12-22 15:35

import django_currentuser.middleware
import django_tenants.postgresql_backend.base

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tenant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                (
                    'schema_name',
                    models.CharField(
                        db_index=True,
                        max_length=63,
                        unique=True,
                        validators=[django_tenants.postgresql_backend.base._check_schema_name],  # noqa: SLF001
                    ),
                ),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                (
                    'tenant_type',
                    models.CharField(
                        choices=[('public', 'public'), ('project', 'project')], default='project', max_length=100
                    ),
                ),
                (
                    'creation_user',
                    models.ForeignKey(
                        default=django_currentuser.middleware.get_current_user,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='%(app_label)s_%(class)s_creation',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ('members', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                (
                    'modification_user',
                    models.ForeignKey(
                        default=django_currentuser.middleware.get_current_user,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='%(app_label)s_%(class)s_modification',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(db_index=True, max_length=253, unique=True)),
                ('is_primary', models.BooleanField(db_index=True, default=True)),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, null=True)),
                (
                    'creation_user',
                    models.ForeignKey(
                        default=django_currentuser.middleware.get_current_user,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='%(app_label)s_%(class)s_creation',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'modification_user',
                    models.ForeignKey(
                        default=django_currentuser.middleware.get_current_user,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='%(app_label)s_%(class)s_modification',
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    'tenant',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='tenants.tenant'
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
