# Generated by Django 2.2.1 on 2019-06-04 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0119_attachment_file_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='file_name',
            field=models.CharField(default='somthing', max_length=255),
            preserve_default=False,
        ),
    ]
