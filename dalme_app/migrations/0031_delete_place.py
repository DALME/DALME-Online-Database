# Generated by Django 4.2.2 on 2023-12-14 10:45

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('dalme_app', '0030_delete_publication'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name='Place',
                ),
            ],
            database_operations=[
                migrations.AlterModelTable(
                    name='Place',
                    table='ida_place',
                ),
            ],
        ),
    ]