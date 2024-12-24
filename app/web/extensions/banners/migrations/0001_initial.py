# Generated by Django 5.1.4 on 2024-12-23 20:33

import wagtail.fields

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('wagtailcore', '0094_alter_page_locale'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(db_index=True, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(help_text='The title of the banner.', max_length=255)),
                ('show_title', models.BooleanField(default=True, help_text='title?', verbose_name='Show')),
                ('info', wagtail.fields.RichTextField(help_text='The main content of the banner.')),
                (
                    'url',
                    models.URLField(
                        blank=True, help_text='If included a link to the URL will be added to the title of the banner.'
                    ),
                ),
                (
                    'color',
                    models.CharField(
                        choices=[
                            ('default', 'Default'),
                            ('blue', 'Blue'),
                            ('green', 'Green'),
                            ('orange', 'Orange'),
                            ('purple', 'Purple'),
                            ('red', 'Red'),
                        ],
                        default='default',
                        help_text='Choose scheme.',
                        max_length=10,
                    ),
                ),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                (
                    'page',
                    models.ForeignKey(
                        blank=True,
                        help_text='If selected, a "Learn more..." button linking to a page will be included in the banner.',
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='banner',
                        to='wagtailcore.page',
                    ),
                ),
            ],
        ),
    ]
