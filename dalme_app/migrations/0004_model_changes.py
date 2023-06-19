import django_currentuser.middleware

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):  # noqa: D101
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0003_collections_refactoring'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Attribute_type',
            new_name='AttributeType',
        ),
        migrations.RenameModel(
            old_name='Source_pages',
            new_name='SourcePages',
        ),
        migrations.RenameModel(
            old_name='Content_type',
            new_name='ContentTypeExtended',
        ),
        migrations.RenameModel(
            old_name='Entity_phrase',
            new_name='EntityPhrase',
        ),
        migrations.RenameModel(
            old_name='Object_attribute',
            new_name='ObjectAttribute',
        ),
        migrations.RenameModel(
            old_name='Source_credit',
            new_name='SourceCredits',
        ),
        migrations.RenameModel(
            old_name='Work_log',
            new_name='WorkLog',
        ),
        migrations.RenameModel(
            old_name='Content_attributes',
            new_name='ContentAttributeTypes',
        ),
        migrations.CreateModel(
            name='OptionsList',
            fields=[
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                (
                    'type',
                    models.CharField(
                        choices=[
                            ('db_records', 'DB Records'),
                            ('field_choices', 'Field Choices'),
                            ('static_list', 'Static List'),
                        ],
                        max_length=15,
                    ),
                ),
                ('description', models.TextField()),
                ('payload', models.JSONField()),
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
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='attributetype',
            name='same_as',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='dalme_app.attributetype',
            ),
        ),
        migrations.AlterField(
            model_name='attributetype',
            name='creation_user',
            field=models.ForeignKey(
                default=django_currentuser.middleware.get_current_user,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='%(app_label)s_%(class)s_creation',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='attributetype',
            name='modification_user',
            field=models.ForeignKey(
                default=django_currentuser.middleware.get_current_user,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='%(app_label)s_%(class)s_modification',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='attributetype',
            name='data_type',
            field=models.CharField(
                choices=[
                    ('DATE', 'DATE (date)'),
                    ('DEC', 'DEC (decimal)'),
                    ('INT', 'INT (integer)'),
                    ('STR', 'STR (string)'),
                    ('TXT', 'TXT (text)'),
                    ('JSON', 'JSON (data)'),
                    ('FK-UUID', 'FK-UUID (DALME record)'),
                    ('FK-INT', 'FK-INT (DALME record)'),
                    ('RREL', 'RREL (reverse relation)'),
                ],
                max_length=15,
            ),
        ),
        migrations.RemoveField(
            model_name='contenttypeextended',
            name='content_class',
        ),
        migrations.RemoveField(
            model_name='contenttypeextended',
            name='r1_inheritance',
        ),
        migrations.RemoveField(
            model_name='contenttypeextended',
            name='r2_inheritance',
        ),
        migrations.AlterField(
            model_name='contenttypeextended',
            name='creation_user',
            field=models.ForeignKey(
                default=django_currentuser.middleware.get_current_user,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='%(app_label)s_%(class)s_creation',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='contenttypeextended',
            name='modification_user',
            field=models.ForeignKey(
                default=django_currentuser.middleware.get_current_user,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='%(app_label)s_%(class)s_modification',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='contenttypeextended',
            name='attribute_types',
            field=models.ManyToManyField(
                through='dalme_app.ContentAttributeTypes',
                to='dalme_app.attributetype',
            ),
        ),
        migrations.AddField(
            model_name='contenttypeextended',
            name='content_type',
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='extended',
                to='contenttypes.contenttype',
            ),
        ),
        migrations.AddField(
            model_name='contenttypeextended',
            name='parents_list',
            field=models.ManyToManyField(
                related_name='children',
                to='dalme_app.contenttypeextended',
            ),
        ),
        migrations.AddField(
            model_name='contenttypeextended',
            name='can_view',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contenttypeextended',
            name='can_edit',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contenttypeextended',
            name='can_delete',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contenttypeextended',
            name='can_add',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contenttypeextended',
            name='can_remove',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='contenttypeextended',
            name='is_abstract',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='Content_class',
        ),
        migrations.AlterField(
            model_name='sourcepages',
            name='creation_user',
            field=models.ForeignKey(
                default=django_currentuser.middleware.get_current_user,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='%(app_label)s_%(class)s_creation',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='sourcepages',
            name='modification_user',
            field=models.ForeignKey(
                default=django_currentuser.middleware.get_current_user,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='%(app_label)s_%(class)s_modification',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterModelOptions(
            name='rightspolicy',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='groupproperties',
            name='type',
            field=models.IntegerField(
                choices=[(1, 'Admin'), (2, 'DAM'), (3, 'Team'), (4, 'Knowledge Base'), (5, 'Website')],
            ),
        ),
        migrations.AlterField(
            model_name='attribute',
            name='attribute_type',
            field=models.ForeignKey(
                db_column='attribute_type',
                on_delete=django.db.models.deletion.CASCADE,
                to='dalme_app.attributetype',
            ),
        ),
        migrations.AlterField(
            model_name='contentattributetypes',
            name='attribute_type',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='content_types',
                to='dalme_app.attributetype',
            ),
        ),
        migrations.AlterField(
            model_name='contentattributetypes',
            name='content_type',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='attribute_type_list',
                to='dalme_app.contenttypeextended',
            ),
        ),
        migrations.AlterField(
            model_name='source',
            name='pages',
            field=models.ManyToManyField(
                db_index=True,
                through='dalme_app.SourcePages',
                to='dalme_app.page',
            ),
        ),
        migrations.AlterField(
            model_name='source',
            name='type',
            field=models.ForeignKey(
                db_column='type',
                on_delete=django.db.models.deletion.PROTECT,
                to='dalme_app.contenttypeextended',
            ),
        ),
        migrations.AlterField(
            model_name='task',
            name='workset',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='dalme_app.collection',
            ),
        ),
        migrations.AlterModelOptions(
            name='publicregister',
            options={'ordering': ['created']},
        ),
        migrations.RenameField(
            model_name='objectattribute',
            old_name='object',
            new_name='obj',
        ),
        migrations.RenameField(
            model_name='scope',
            old_name='range',
            new_name='scope_range',
        ),
        migrations.RenameField(
            model_name='scope',
            old_name='type',
            new_name='scope_type',
        ),
        migrations.AddField(
            model_name='task',
            name='assignees',
            field=models.ManyToManyField(blank=True, related_name='task_assignations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='task',
            name='completed_by',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='completed_tasks',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name='task',
            name='files',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='dalme_app.attachment'),
        ),
        migrations.AddField(
            model_name='task',
            name='resources',
            field=models.ManyToManyField(blank=True, related_name='tasks', to='dalme_app.collection'),
        ),
        migrations.AlterField(
            model_name='attachment',
            name='type',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='attributereference',
            name='term_type',
            field=models.CharField(blank=True, max_length=55),
        ),
        migrations.AlterField(
            model_name='comment',
            name='body',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='object_id',
            field=models.CharField(db_index=True, default='', max_length=55),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contenttypeextended',
            name='can_view',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='contenttypeextended',
            name='parents',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='languagereference',
            name='iso6393',
            field=models.CharField(blank=True, default='', max_length=25, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='page',
            name='canvas',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rightspolicy',
            name='licence',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rightspolicy',
            name='rights',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='rightspolicy',
            name='rights_holder',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sourcecredits',
            name='note',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sourcepages',
            name='source',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='folios',
                to='dalme_app.source',
            ),
        ),
        migrations.AlterField(
            model_name='sourcepages',
            name='transcription',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='folios',
                to='dalme_app.transcription',
            ),
        ),
        migrations.AlterField(
            model_name='tag',
            name='object_id',
            field=models.CharField(blank=True, db_index=True, default='', max_length=55),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag',
            field=models.CharField(blank=True, default='', max_length=55),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tag',
            name='tag_group',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='task',
            name='position',
        ),
        migrations.AlterField(
            model_name='task',
            name='url',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='url',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='transcription',
            name='transcription',
            field=models.TextField(blank=True),
        ),
        migrations.RenameField(
            model_name='tasklist',
            old_name='group',
            new_name='team_link',
        ),
        migrations.AlterField(
            model_name='tasklist',
            name='team_link',
            field=models.ForeignKey(
                limit_choices_to={'properties__type': 3},
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='team_tasklist',
                to='auth.group',
            ),
        ),
        migrations.AlterUniqueTogether(
            name='tasklist',
            unique_together={('team_link', 'slug')},
        ),
        migrations.AlterField(
            model_name='agent',
            name='user',
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='agent_record',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='source_content_type',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='rel_sources',
                to='contenttypes.contenttype',
            ),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='source_object_id',
            field=models.CharField(db_index=True, default=None, max_length=36),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='relationship',
            name='target_content_type',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='rel_targets',
                to='contenttypes.contenttype',
            ),
        ),
        migrations.AlterField(
            model_name='relationship',
            name='target_object_id',
            field=models.CharField(db_index=True, default=None, max_length=36),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='RelationshipType',
            fields=[
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=55, unique=True)),
                ('description', models.TextField()),
                ('source', models.CharField(blank=True, max_length=255)),
                ('is_directed', models.BooleanField(default=False)),
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
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AddField(
            model_name='relationship',
            name='rel_type',
            field=models.ForeignKey(
                db_column='rel_type',
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name='relationships',
                to='dalme_app.relationshiptype',
            ),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='relationship',
            name='scope',
        ),
        migrations.RemoveField(
            model_name='scope',
            name='scope_range',
        ),
        migrations.AddField(
            model_name='relationship',
            name='scopes',
            field=models.ManyToManyField(db_index=True, to='dalme_app.scope'),
        ),
        migrations.AddField(
            model_name='scope',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='scope',
            name='parameters',
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ScopeType',
            fields=[
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('short_name', models.CharField(max_length=55, unique=True)),
                ('description', models.TextField()),
                ('source', models.CharField(blank=True, max_length=255)),
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
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.AlterField(
            model_name='scope',
            name='scope_type',
            field=models.ForeignKey(
                db_column='scope_type',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='scopes',
                to='dalme_app.scopetype',
            ),
        ),
        migrations.AddField(
            model_name='contentattributetypes',
            name='description_override',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='contentattributetypes',
            name='label_override',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='attributetype',
            name='is_local',
            field=models.BooleanField(default=False),
        ),
        migrations.RenameField(
            model_name='contentattributetypes',
            old_name='required',
            new_name='is_required',
        ),
        migrations.AlterUniqueTogether(
            name='contentattributetypes',
            unique_together={('content_type', 'attribute_type')},
        ),
    ]
