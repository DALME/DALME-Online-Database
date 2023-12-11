# Generated by Django 4.2.2 on 2023-12-08 15:21
import django_currentuser.middleware
import django_tenants.postgresql_backend.base

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                (
                    'is_superuser',
                    models.BooleanField(
                        default=False,
                        help_text='Designates that this user has all permissions without explicitly assigning them.',
                        verbose_name='superuser status',
                    ),
                ),
                (
                    'username',
                    models.CharField(
                        error_messages={'unique': 'A user with that username already exists.'},
                        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
                        max_length=150,
                        unique=True,
                        validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
                        verbose_name='username',
                    ),
                ),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                (
                    'is_staff',
                    models.BooleanField(
                        default=False,
                        help_text='Designates whether the user can log into this admin site.',
                        verbose_name='staff status',
                    ),
                ),
                (
                    'is_active',
                    models.BooleanField(
                        default=True,
                        help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
                        verbose_name='active',
                    ),
                ),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                (
                    'groups',
                    models.ManyToManyField(
                        blank=True,
                        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
                        related_name='user_set',
                        related_query_name='user',
                        to='auth.Group',
                        verbose_name='groups',
                    ),
                ),
                (
                    'user_permissions',
                    models.ManyToManyField(
                        blank=True,
                        help_text='Specific permissions for this user.',
                        related_name='user_set',
                        related_query_name='user',
                        to='auth.Permission',
                        verbose_name='user permissions',
                    ),
                ),
            ],
            options={
                'db_table': 'auth_user',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Tenant',
            fields=[
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
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255, unique=True)),
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
                ('domain', models.CharField(db_index=True, max_length=253, unique=True)),
                ('is_primary', models.BooleanField(db_index=True, default=True)),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False, unique=True)),
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
                        on_delete=django.db.models.deletion.CASCADE, related_name='domains', to='ida.tenant'
                    ),
                ),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
