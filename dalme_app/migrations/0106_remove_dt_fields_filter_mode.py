# Generated by Django 2.2.1 on 2019-06-02 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0105_auto_20190601_1536'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dt_fields',
            name='filter_mode',
        ),
    ]
