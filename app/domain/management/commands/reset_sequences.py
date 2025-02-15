"""Management command to reset db sequences for a migration deploy."""

import os

os.environ['DJANGO_COLORS'] = 'nocolor'

from StringIO import StringIO

from django.apps import apps
from django.core.management import call_command
from django.db import connection

commands = StringIO()
cursor = connection.cursor()

for app in apps.get_app_configs():
    call_command('sqlsequencereset', app.label, stdout=commands)

cursor.execute(commands.getvalue())
