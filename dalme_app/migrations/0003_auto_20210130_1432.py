# Generated by Django 3.1.2 on 2021-01-30 19:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0002_savedsearch'),
    ]

    operations = [
        migrations.RenameField(
            model_name='place',
            old_name='std_name',
            new_name='standard_name',
        ),
        migrations.RemoveField(
            model_name='entity_phrase',
            name='phrase',
        ),
        migrations.RemoveField(
            model_name='entity_phrase',
            name='type',
        ),
        migrations.AddField(
            model_name='attribute',
            name='value_DEC',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='place',
            name='locale',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dalme_app.localereference'),
        ),
        migrations.AddField(
            model_name='place',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='notes',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='agent',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='agent', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='attribute_type',
            name='data_type',
            field=models.CharField(choices=[('DATE', 'DATE (date)'), ('DEC', 'DEC (decimal)'), ('INT', 'INT (integer)'), ('STR', 'STR (string)'), ('TXT', 'TXT (text)'), ('FK-UUID', 'FK-UUID (DALME record)'), ('FK-INT', 'FK-INT (DALME record)')], max_length=15),
        ),
        migrations.AlterField(
            model_name='place',
            name='type',
            field=models.IntegerField(db_index=True, null=True),
        ),
    ]