import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):  # noqa: D101
    atomic = False
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0004_redirect_fields'),
    ]

    operations = [
        # Agent
        migrations.RenameField(
            model_name='agent',
            old_name='type',
            new_name='agent_type',
        ),
        migrations.RenameField(
            model_name='agent',
            old_name='standard_name',
            new_name='name',
        ),
        # Attribute
        migrations.AlterField(
            model_name='attribute',
            name='object_id',
            field=models.CharField(db_index=True, default='', max_length=36),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='attribute',
            unique_together=set(),
        ),
        # AttributeType
        migrations.AlterField(
            model_name='attributetype',
            name='data_type',
            field=models.CharField(
                choices=[
                    ('BOOL', 'BOOL (boolean)'),
                    ('DATE', 'DATE (date)'),
                    ('DEC', 'DEC (decimal)'),
                    ('FKEY', 'FKEY (foreign key)'),
                    ('INT', 'INT (integer)'),
                    ('JSON', 'JSON (data)'),
                    ('STR', 'STR (string)'),
                    ('TXT', 'TXT (text)'),
                    ('FK-UUID', 'FK-UUID (DALME record)'),
                    ('FK-INT', 'FK-INT (DALME record)'),
                ],
                max_length=15,
            ),
        ),
        migrations.AlterField(
            model_name='attributetype',
            name='source',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='attributetype',
            name='is_local',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='attributetype',
            name='options',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='dalme_app.optionslist',
            ),
        ),
        # AttributeReference
        migrations.AlterField(
            model_name='attributereference',
            name='term_type',
            field=models.CharField(blank=True, max_length=55),
        ),
        # Attachment
        migrations.RenameField(
            model_name='attachment',
            old_name='file',
            new_name='filefield',
        ),
        migrations.RenameField(
            model_name='attachment',
            old_name='type',
            new_name='filetype',
        ),
        # ContentAttributes
        migrations.AddField(
            model_name='contentattributes',
            name='content_type',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='attributes_list',
                to='dalme_app.contenttypeextended',
            ),
        ),
        migrations.AlterUniqueTogether(
            name='contentattributes',
            unique_together={('content_type', 'attribute_type')},
        ),
        # Comment
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
        # Folio
        migrations.RenameField(
            model_name='folio',
            old_name='source',
            new_name='record',
        ),
        # GroupProperties
        migrations.RenameField(
            model_name='groupproperties',
            old_name='type',
            new_name='group_type',
        ),
        # LanguageReference
        migrations.AlterField(
            model_name='languagereference',
            name='iso6393',
            field=models.CharField(blank=True, default='', max_length=25, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='languagereference',
            name='is_dialect',
            field=models.BooleanField(default=False),
        ),
        # ObjectAttribute
        migrations.RenameField(
            model_name='objectattribute',
            old_name='object',
            new_name='obj',
        ),
        # Page
        migrations.AlterField(
            model_name='page',
            name='canvas',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        # Place
        migrations.RenameField(
            model_name='place',
            old_name='standard_name',
            new_name='name',
        ),
        migrations.AddField(
            model_name='place',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dalme_app.location'),
        ),
        # PublicRegister
        migrations.AlterModelOptions(
            name='publicregister',
            options={'ordering': ['created']},
        ),
        # Record
        migrations.RenameField(
            model_name='record',
            old_name='parent',
            new_name='old_parent',
        ),
        migrations.AddField(
            model_name='record',
            name='parent_id',
            field=models.CharField(db_index=True, max_length=36, null=True),
        ),
        migrations.AddField(
            model_name='record',
            name='parent_type',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to='contenttypes.contenttype',
            ),
        ),
        # Relationship
        migrations.RemoveField(
            model_name='relationship',
            name='scope',
        ),
        migrations.AddField(
            model_name='relationship',
            name='scopes',
            field=models.ManyToManyField(db_index=True, to='dalme_app.scope'),
        ),
        # RightsPolicy
        migrations.AlterModelOptions(
            name='rightspolicy',
            options={'ordering': ['name']},
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
        # Scope
        migrations.RenameField(
            model_name='scope',
            old_name='range',
            new_name='scope_range',
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
        # Tag
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
        # Task
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
            model_name='task',
            name='description',
            field=models.TextField(blank=True, default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='task',
            name='url',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=False,
        ),
        # TaskList
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
        # Ticket
        migrations.AddField(
            model_name='ticket',
            name='files',
            field=models.ManyToManyField(
                blank=True,
                related_name='tickets',
                to='dalme_app.attachment',
            ),
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
        # Transcription
        migrations.AlterField(
            model_name='transcription',
            name='transcription',
            field=models.TextField(blank=True),
        ),
        # Workflow
        migrations.RenameField(
            model_name='workflow',
            old_name='source',
            new_name='record',
        ),
        # Worklog
        migrations.RenameField(
            model_name='worklog',
            old_name='source',
            new_name='record',
        ),
    ]
