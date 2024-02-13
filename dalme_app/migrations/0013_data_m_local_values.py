from django.conf import settings
from django.db import migrations


def migrate_local_values(apps, schema_editor):
    """Migrate local values to attributes."""
    Record = apps.get_model('dalme_app', 'Record')  # noqa: N806
    AttributeType = apps.get_model('dalme_app', 'AttributeType')  # noqa: N806
    ContentType = apps.get_model('contenttypes', 'ContentType')  # noqa: N806
    AttributeValueBool = apps.get_model('dalme_app', 'AttributeValueBool')  # noqa: N806
    # apps.get_model("dalme_app", "AttributeValueFkey")
    # apps.get_model("dalme_app", "AttributeValueStr")

    # Record:
    has_inv_type = AttributeType.objects.get(short_name='has_inventory')

    record_ct = ContentType.objects.get(app_label='dalme_app', model='record')
    ContentType.objects.get(app_label='auth', model='user')

    print('\n\nMigrating local values to attributes...', end='')  # noqa: T201

    for record in Record.objects.all():
        has_inv = AttributeValueBool(
            content_type=record_ct,
            object_id=record.id,
            attribute_type=has_inv_type,
            value=record.has_inventory,
            creation_user=record.creation_user,
            modification_user=record.modification_user,
            creation_timestamp=record.creation_timestamp,
            modification_timestamp=record.modification_timestamp,
        )
        has_inv.save()
        # has_inv.save_base(raw=True)

    print(' \033[94m\033[1mOK\033[0m')  # noqa: T201
    print('  Overall migration...', end='')  # noqa: T201


class Migration(migrations.Migration):
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0012_data_m_atypes'),
    ]

    operations = [
        migrations.RunPython(migrate_local_values),
    ]
