# Generated by Django 2.0.5 on 2018-07-02 14:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0004_m2m_source_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='canvas',
            field=models.TextField(null=True),
        ),
    ]