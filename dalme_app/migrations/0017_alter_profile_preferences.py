# Generated by Django 4.2.2 on 2023-12-13 13:54
from django.db import migrations, models

from ida.models.user import get_default_preferences


class Migration(migrations.Migration):
    dependencies = [
        ('dalme_app', '0016_attachment_tenant_collection_tenant_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='preferences',
            field=models.JSONField(default=get_default_preferences),
        ),
    ]