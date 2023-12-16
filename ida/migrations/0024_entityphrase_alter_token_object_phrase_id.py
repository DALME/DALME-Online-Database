# Generated by Django 4.2.2 on 2023-12-16 12:50

import uuid

import django_currentuser.middleware

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('ida', '0023_location_alter_organization_location_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='EntityPhrase',
                    fields=[
                        ('creation_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                        ('modification_timestamp', models.DateTimeField(auto_now=True, null=True)),
                        (
                            'id',
                            models.UUIDField(
                                db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                            ),
                        ),
                        ('object_id', models.UUIDField(db_index=True, null=True)),
                        (
                            'content_type',
                            models.ForeignKey(
                                null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'
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
                            'transcription_id',
                            models.ForeignKey(
                                on_delete=django.db.models.deletion.CASCADE,
                                related_name='entity_phrases',
                                to='ida.transcription',
                            ),
                        ),
                    ],
                    options={
                        'abstract': False,
                    },
                ),
                migrations.AlterField(
                    model_name='token',
                    name='object_phrase_id',
                    field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ida.entityphrase'),
                ),
            ],
            database_operations=[],
        ),
    ]
