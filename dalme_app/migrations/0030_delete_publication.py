# Generated by Django 4.2.2 on 2023-12-14 10:40
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('dalme_app', '0029_remove_relationshiptype_creation_user_and_more'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.DeleteModel(
                    name='Publication',
                ),
            ],
            database_operations=[
                migrations.AlterModelTable(
                    name='Publication',
                    table='ida_publication',
                ),
            ],
        ),
    ]