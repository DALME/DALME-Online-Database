# Generated by Django 3.1.2 on 2021-01-29 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0002_savedsearch'),
        ('dalme_public', '0010_auto_20210118_1157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='essay',
            name='source',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='essays', to='dalme_app.source'),
        ),
        migrations.AlterField(
            model_name='essay',
            name='source_set',
            field=models.ForeignKey(blank=True, help_text='Optional, select a particular public set for the source associated with this essay. The source must be a member of the set chosen or the page will not validate.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='essays', to='dalme_app.set'),
        ),
        migrations.AlterField(
            model_name='featuredinventory',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='featured_inventories', to='dalme_app.source'),
        ),
        migrations.AlterField(
            model_name='featuredinventory',
            name='source_set',
            field=models.ForeignKey(blank=True, help_text='Optional, select a particular public set for the source associated with this inventory. The source must be a member of the set chosen or the page will not validate.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='featured_inventories', to='dalme_app.set'),
        ),
        migrations.AlterField(
            model_name='featuredobject',
            name='source',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='featured_objects', to='dalme_app.source'),
        ),
        migrations.AlterField(
            model_name='featuredobject',
            name='source_set',
            field=models.ForeignKey(blank=True, help_text='Optional, select a particular public set for the source associated with this object. The source must be a member of the set chosen or the page will not validate.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='featured_objects', to='dalme_app.set'),
        ),
    ]