# Generated by Django 4.2.2 on 2024-03-01 17:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('ida', '0005_alter_rightspolicy_licence'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='url',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
