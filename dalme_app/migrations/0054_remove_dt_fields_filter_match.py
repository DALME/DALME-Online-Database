# Generated by Django 2.1.7 on 2019-05-05 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0053_dt_fields_filter_match'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dt_fields',
            name='filter_match',
        ),
    ]