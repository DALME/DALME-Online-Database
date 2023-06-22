from django.conf import settings
from django.contrib.contenttypes.management import create_contenttypes
from django.db import migrations


def update_content_types(apps, schema_editor):  # noqa: ARG001
    """Update content types."""
    app_config = apps.get_app_config('dalme_app')
    app_config.models_module = True
    print('\n')  # noqa: T201
    create_contenttypes(app_config)
    print('  Overall migration...', end='')  # noqa: T201


class Migration(migrations.Migration):  # noqa: D101
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0005_field_changes'),
    ]
    operations = [
        migrations.RunPython(update_content_types),
    ]
