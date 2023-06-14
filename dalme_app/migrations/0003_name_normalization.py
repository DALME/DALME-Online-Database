import django_currentuser.middleware

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):  # noqa: D101
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0002_collections_refactoring'),
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
        migrations.AlterField(
            model_name='attributetype',
            name='same_as',
            field=models.ForeignKey(
                db_column='same_as',
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
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
            model_name='contentattributetypes',
            name='options_source',
            field=models.JSONField(null=True),
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
        migrations.AlterField(
            model_name='task',
            name='position',
            field=models.CharField(blank=True, max_length=255),
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
    ]
