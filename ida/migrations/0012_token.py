# Generated by Django 4.2.2 on 2023-12-13 17:57
import uuid

import django_currentuser.middleware

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dalme_app', '0025_delete_token'),
        ('ida', '0011_transcription'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.CreateModel(
                    name='Token',
                    fields=[
                        ('creation_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                        ('modification_timestamp', models.DateTimeField(auto_now=True, null=True)),
                        (
                            'id',
                            models.UUIDField(
                                db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False
                            ),
                        ),
                        ('raw_token', models.CharField(max_length=255)),
                        ('clean_token', models.CharField(max_length=55)),
                        ('order', models.IntegerField(db_index=True)),
                        ('flags', models.CharField(max_length=10)),
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
                            'object_phrase_id',
                            models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dalme_app.entityphrase'),
                        ),
                        (
                            'wordform_id',
                            models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ida.wordform'),
                        ),
                    ],
                    options={
                        'abstract': False,
                    },
                ),
            ],
            database_operations=[],
        ),
    ]
