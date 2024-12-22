# Generated by Django 5.0.4 on 2024-12-22 15:35

import modelcluster.fields
import wagtail.fields

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('wagtailcore', '0093_uploadedfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Footnote',
            fields=[
                ('sort_order', models.IntegerField(blank=True, editable=False, null=True)),
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('text', wagtail.fields.RichTextField()),
                (
                    'page',
                    modelcluster.fields.ParentalKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='footnotes',
                        to='wagtailcore.page',
                    ),
                ),
            ],
            options={
                'unique_together': {('page', 'id')},
            },
        ),
    ]
