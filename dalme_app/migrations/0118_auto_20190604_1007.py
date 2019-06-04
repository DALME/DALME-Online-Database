# Generated by Django 2.2.1 on 2019-06-04 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0117_attachment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attachment',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='attachment',
            name='object_id',
        ),
        migrations.AddField(
            model_name='task',
            name='file',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dalme_app.Attachment'),
        ),
    ]
