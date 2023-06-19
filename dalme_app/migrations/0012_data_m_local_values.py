from django.conf import settings
from django.db import migrations


def migrate_local_values(apps, schema_editor):  # noqa: ARG001
    """Migrate local values to attributes."""
    Source = apps.get_model("dalme_app", "Source")  # noqa: N806
    AttributeType = apps.get_model("dalme_app", "AttributeType")  # noqa: N806
    ContentType = apps.get_model('contenttypes', 'ContentType')  # noqa: N806
    AttributeValueBool = apps.get_model("dalme_app", "AttributeValueBool")  # noqa: N806
    AttributeValueFkey = apps.get_model("dalme_app", "AttributeValueFkey")  # noqa: N806
    apps.get_model("dalme_app", "AttributeValueStr")

    # Source:
    parent_type = AttributeType.objects.get(short_name='parent')
    has_inv_type = AttributeType.objects.get(short_name='has_inventory')

    source_ct = ContentType.objects.get(app_label='dalme_app', model='source')
    ContentType.objects.get(app_label='auth', model='user')

    for source in Source.objects.all():
        if source.parent:
            parent = AttributeValueFkey(
                content_type=source_ct,
                object_id=source.id,
                attribute_type=parent_type,
                target_content_type=source_ct,
                target_id=source.parent.id,
                creation_user=source.creation_user,
                modification_user=source.modification_user,
                creation_timestamp=source.creation_timestamp,
                modification_timestamp=source.modification_timestamp,
            )
            parent.save()
            # parent.save_base(raw=True)

        has_inv = AttributeValueBool(
            content_type=source_ct,
            object_id=source.id,
            attribute_type=has_inv_type,
            value=source.has_inventory,
            creation_user=source.creation_user,
            modification_user=source.modification_user,
            creation_timestamp=source.creation_timestamp,
            modification_timestamp=source.modification_timestamp,
        )
        has_inv.save()
        # has_inv.save_base(raw=True)


class Migration(migrations.Migration):  # noqa: D101
    atomic = False
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0011_data_m_options_types'),
    ]

    operations = [
        migrations.RunPython(migrate_local_values),
    ]
