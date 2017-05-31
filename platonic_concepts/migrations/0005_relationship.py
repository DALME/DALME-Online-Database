# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-05-31 20:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import platonic_concepts.models


class Migration(migrations.Migration):

    dependencies = [
        ('platonic_concepts', '0004_auto_20170531_1951'),
    ]

    operations = [
        migrations.CreateModel(
            name='Relationship',
            fields=[
                ('_id', models.CharField(db_column='id', default=platonic_concepts.models.make_uuid, max_length=36, primary_key=True, serialize=False, unique=True)),
                ('relationship', models.CharField(max_length=36)),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='platonic_concepts.PlatonicConcept')),
                ('target', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='target', to='platonic_concepts.PlatonicConcept')),
            ],
        ),
    ]
