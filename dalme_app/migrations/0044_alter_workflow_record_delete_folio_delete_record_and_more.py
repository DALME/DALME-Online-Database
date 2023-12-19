# Generated by Django 4.2.2 on 2023-12-18 11:12
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('dalme_public', '0005_alter_essay_source_alter_featuredinventory_source_and_more'),
        ('dalme_app', '0043_remove_folio_creation_user_and_more'),
        ('ida', '0029_folio_recordgroup_record_folio_record_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name='workflow',
                    name='record',
                    field=models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name='workflow',
                        serialize=False,
                        to='ida.record',
                    ),
                ),
            ],
            database_operations=[],
        ),
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name='Folio',
                ),
                migrations.DeleteModel(
                    name='Record',
                ),
                migrations.DeleteModel(
                    name='RecordGroup',
                ),
            ],
            database_operations=[
                migrations.AlterModelTable(
                    name='Folio',
                    table='ida_folio',
                ),
                migrations.AlterModelTable(
                    name='Record',
                    table='ida_record',
                ),
                migrations.AlterModelTable(
                    name='RecordGroup',
                    table='ida_recordgroup',
                ),
            ],
        ),
    ]