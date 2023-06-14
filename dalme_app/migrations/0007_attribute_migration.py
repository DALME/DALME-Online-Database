from django.conf import settings
from django.db import migrations


def migrate_attributes(apps, schema_editor):  # noqa: ARG001
    """Migrate attribute values to new system."""
    ContentType = apps.get_model('contenttypes', 'ContentType')  # noqa: N806
    Attribute = apps.get_model("dalme_app", "Attribute")  # noqa: N806
    AttributeValueDate = apps.get_model("dalme_app", "AttributeValueDate")  # noqa: N806
    AttributeValueDec = apps.get_model("dalme_app", "AttributeValueDec")  # noqa: N806
    AttributeValueInt = apps.get_model("dalme_app", "AttributeValueInt")  # noqa: N806
    AttributeValueJson = apps.get_model("dalme_app", "AttributeValueJson")  # noqa: N806
    AttributeValueStr = apps.get_model("dalme_app", "AttributeValueStr")  # noqa: N806
    AttributeValueTxt = apps.get_model("dalme_app", "AttributeValueTxt")  # noqa: N806
    AttributeValueFkey = apps.get_model("dalme_app", "AttributeValueFkey")  # noqa: N806
    CountryReference = apps.get_model("dalme_app", "CountryReference")  # noqa: N806, F841
    LanguageReference = apps.get_model("dalme_app", "LanguageReference")  # noqa: N806, F841
    LocaleReference = apps.get_model("dalme_app", "LocaleReference")  # noqa: N806, F841
    RightsPolicy = apps.get_model("dalme_app", "RightsPolicy")  # noqa: N806, F841

    for att in Attribute.objects.all():
        dtype = att.attribute_type.data_type

        if dtype == 'DATE':
            new_val = AttributeValueDate(
                attribute_ptr=att,
                value_day=att.value_DATE_d,
                value_month=att.value_DATE_m,
                value_year=att.value_DATE_y,
                value_date=att.value_DATE,
                value_str=att.value_STR,
            )
            new_val.save_base(raw=True)

        elif dtype == 'DEC':
            new_val = AttributeValueDec(
                attribute_ptr=att,
                value=att.value_DEC,
            )
            new_val.save_base(raw=True)

        elif dtype == 'INT':
            new_val = AttributeValueInt(
                attribute_ptr=att,
                value=att.value_INT,
            )
            new_val.save_base(raw=True)

        elif dtype == 'JSON':
            new_val = AttributeValueJson(
                attribute_ptr=att,
                value=att.value_JSON,
            )
            new_val.save_base(raw=True)

        elif dtype == 'STR':
            new_val = AttributeValueStr(
                attribute_ptr=att,
                value=att.value_STR,
            )
            new_val.save_base(raw=True)

        elif dtype == 'TXT':
            new_val = AttributeValueTxt(
                attribute_ptr=att,
                value=att.value_TXT,
            )
            new_val.save_base(raw=True)

        elif dtype in ['FK-UUID', 'FK-INT'] and att.value_JSON is not None:
            _id = att.value_JSON['id']
            obj_class = att.value_JSON['class']
            obj_ct = ContentType.objects.get(app_label='dalme_app', model=obj_class.lower())

            new_val = AttributeValueFkey(
                attribute_ptr=att,
                target_content_type=obj_ct,
                target_id=_id,
            )
            new_val.save_base(raw=True)

            att.attribute_type.data_type = 'FKEY'
            att.save()


class Migration(migrations.Migration):  # noqa: D101
    atomic = False
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0006_data_migrations'),
    ]

    operations = [
        migrations.RunPython(migrate_attributes),
    ]
