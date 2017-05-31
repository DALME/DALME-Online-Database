# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-31 18:31
from __future__ import unicode_literals

from django.db import migrations, models
import platonic_concepts.models


class Migration(migrations.Migration):

    dependencies = [
        ('platonic_concepts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='platonicconcept',
            name='id',
        ),
        migrations.AlterField(
            model_name='platonicconcept',
            name='_id',
            field=models.CharField(db_column='id', default=platonic_concepts.models.make_uuid, max_length=36, primary_key=True, serialize=False, unique=True),
        ),
    ]
