# Generated by Django 3.1.12 on 2021-09-02 14:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_public', '0011_auto_20210129_0854'),
    ]

    operations = [
        migrations.AddField(
            model_name='essay',
            name='front_page_image',
            field=models.ForeignKey(blank=True, help_text='The image that will display on the front page.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='dalme_public.dalmeimage'),
        ),
        migrations.AddField(
            model_name='featuredinventory',
            name='front_page_image',
            field=models.ForeignKey(blank=True, help_text='The image that will display on the front page.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='dalme_public.dalmeimage'),
        ),
        migrations.AddField(
            model_name='featuredobject',
            name='front_page_image',
            field=models.ForeignKey(blank=True, help_text='The image that will display on the front page.', null=True, on_delete=django.db.models.deletion.SET_NULL, to='dalme_public.dalmeimage'),
        ),
    ]
