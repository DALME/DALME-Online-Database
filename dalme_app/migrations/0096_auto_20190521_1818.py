# Generated by Django 2.1.7 on 2019-05-21 22:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0095_auto_20190521_1639'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dt_fields',
            options={'ordering': ['order']},
        ),
        migrations.RemoveField(
            model_name='attribute',
            name='value_DBR',
        ),
    ]