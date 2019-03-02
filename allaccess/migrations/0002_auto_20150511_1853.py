# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('allaccess', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountaccess',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='accountaccess',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
