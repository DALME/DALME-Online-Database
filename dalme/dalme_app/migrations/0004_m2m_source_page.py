# Generated by Django 2.0.5 on 2018-06-25 18:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dalme_app', '0003_renaming_fk_fields'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='page',
            name='source_id',
        ),
        migrations.AddField(
            model_name='page',
            name='sources',
            field=models.ManyToManyField(db_index=True, to='dalme_app.Source'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
    ]
