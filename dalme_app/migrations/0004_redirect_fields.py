import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0003_rename_and_create_models'),
    ]
    operations = [
        # Change fields
        # Agent
        migrations.AlterField(
            model_name='agent',
            name='old_user',
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='agent_record',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        # Attribute
        migrations.AlterField(
            model_name='attribute',
            name='attribute_type',
            field=models.ForeignKey(
                db_column='attribute_type',
                on_delete=django.db.models.deletion.CASCADE,
                related_name='attributes',
                to='dalme_app.attributetype',
            ),
        ),
        # AttributeType
        migrations.AlterField(
            model_name='attributetype',
            name='same_as',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to='dalme_app.attributetype',
            ),
        ),
        # Attachment
        migrations.AlterField(
            model_name='attachment',
            name='type',
            field=models.CharField(blank=True, default='', max_length=255),
            preserve_default=False,
        ),
        # Folio
        migrations.AlterField(
            model_name='folio',
            name='source',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='folios',
                to='dalme_app.record',
            ),
        ),
        migrations.AlterField(
            model_name='folio',
            name='page',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='records',
                to='dalme_app.page',
            ),
        ),
        migrations.AlterField(
            model_name='folio',
            name='transcription',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='folios',
                to='dalme_app.transcription',
            ),
        ),
        # GroupProperties
        migrations.AlterField(
            model_name='groupproperties',
            name='type',
            field=models.IntegerField(
                choices=[(1, 'Admin'), (2, 'DAM'), (3, 'Team'), (4, 'Knowledge Base'), (5, 'Website')],
            ),
        ),
        # Record
        migrations.AlterField(
            model_name='record',
            name='pages',
            field=models.ManyToManyField(
                db_index=True,
                through='dalme_app.Folio',
                to='dalme_app.page',
            ),
        ),
        # Relationship
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
        # Scope
        migrations.RenameField(
            model_name='scope',
            old_name='type',
            new_name='scope_type',
        ),
        # Task
        migrations.AlterField(
            model_name='task',
            name='workset',
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to='dalme_app.collection',
            ),
        ),
        # TaskList
        migrations.RenameField(
            model_name='tasklist',
            old_name='group',
            new_name='team_link',
        ),
        # Workflow
        migrations.AlterField(
            model_name='workflow',
            name='source',
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                primary_key=True,
                related_name='workflow',
                serialize=False,
                to='dalme_app.record',
            ),
        ),
    ]
