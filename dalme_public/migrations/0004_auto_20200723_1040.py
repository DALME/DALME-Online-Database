# Generated by Django 2.2.4 on 2020-07-23 14:40

from django.db import migrations, models
import wagtail.core.blocks
import wagtail.core.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_public', '0003_auto_20200721_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='footer',
            name='copyright',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='footer',
            name='social',
            field=wagtail.core.fields.StreamField([('social', wagtail.core.blocks.StructBlock([('fa_icon', wagtail.core.blocks.CharBlock()), ('url', wagtail.core.blocks.URLBlock())]))], null=True),
        ),
        migrations.AlterField(
            model_name='collection',
            name='short_title',
            field=models.CharField(blank=True, help_text='An optional short title that will be displayed in certain space constrained contexts.', max_length=63, null=True),
        ),
        migrations.AlterField(
            model_name='collections',
            name='short_title',
            field=models.CharField(blank=True, help_text='An optional short title that will be displayed in certain space constrained contexts.', max_length=63, null=True),
        ),
        migrations.AlterField(
            model_name='features',
            name='short_title',
            field=models.CharField(blank=True, help_text='An optional short title that will be displayed in certain space constrained contexts.', max_length=63, null=True),
        ),
        migrations.AlterField(
            model_name='flat',
            name='short_title',
            field=models.CharField(blank=True, help_text='An optional short title that will be displayed in certain space constrained contexts.', max_length=63, null=True),
        ),
        migrations.AlterField(
            model_name='footer',
            name='pages',
            field=wagtail.core.fields.StreamField([('page', wagtail.core.blocks.StructBlock([('title', wagtail.core.blocks.CharBlock()), ('page', wagtail.core.blocks.PageChooserBlock())]))], null=True),
        ),
        migrations.AlterField(
            model_name='home',
            name='short_title',
            field=models.CharField(blank=True, help_text='An optional short title that will be displayed in certain space constrained contexts.', max_length=63, null=True),
        ),
        migrations.AlterField(
            model_name='section',
            name='short_title',
            field=models.CharField(blank=True, help_text='An optional short title that will be displayed in certain space constrained contexts.', max_length=63, null=True),
        ),
    ]
