# Generated by Django 4.2.2 on 2023-12-13 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ida', '0009_headword'),
        ('dalme_app', '0021_alter_headword_concept_id_alter_object_concept_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name='Headword',
                ),
            ],
            database_operations=[
                migrations.AlterModelTable(
                    name='Headword',
                    table='ida_headword',
                ),
            ],
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='wordform',
                    name='headword_id',
                    field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ida.headword'),
                ),
            ],
            database_operations=[],
        ),
    ]
