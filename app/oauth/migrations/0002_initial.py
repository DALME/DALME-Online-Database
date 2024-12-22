# Generated by Django 5.0.4 on 2024-12-22 15:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('oauth', '0001_initial'),
        ('tenants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupproperties',
            name='tenant',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='tenants.tenant'),
        ),
    ]
