# Generated by Django 2.2.1 on 2019-06-04 15:40

import dalme_app.middleware
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0121_remove_attachment_file_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='tag_type',
            field=models.CharField(choices=[('WF', 'Workflow'), ('C', 'Control'), ('T', 'Ticket')], max_length=2),
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False, unique=True)),
                ('creation_username', models.CharField(blank=True, default=dalme_app.middleware.get_current_username, max_length=255, null=True)),
                ('creation_timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('modification_username', models.CharField(blank=True, default=dalme_app.middleware.get_current_username, max_length=255, null=True)),
                ('modification_timestamp', models.DateTimeField(auto_now=True, null=True)),
                ('title', models.CharField(max_length=140)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.IntegerField(choices=[(0, 'Open'), (1, 'Closed')], max_length=1)),
                ('url', models.CharField(default=None, max_length=255, null=True)),
                ('file', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='dalme_app.Attachment')),
            ],
            options={
                'ordering': ['status', 'creation_timestamp'],
            },
        ),
    ]
