from django.conf import settings
from django.db import migrations


def migrate_attributes(apps, schema_editor):  # noqa: ARG001, PLR0915, C901, PLR0912
    """Migrate attribute values to new system."""
    ContentType = apps.get_model('contenttypes', 'ContentType')  # noqa: N806
    Attribute = apps.get_model("dalme_app", "Attribute")  # noqa: N806
    AttributeType = apps.get_model("dalme_app", "AttributeType")  # noqa: N806
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
    User = apps.get_model("auth", "User")  # noqa: N806

    user_obj = User.objects.get(pk=1)
    attributes = Attribute.objects.all()

    stats = {
        'DATE': {
            'initial': len(attributes.filter(attribute_type__data_type='DATE')),
            'count': 0,
        },
        'DEC': {
            'initial': len(attributes.filter(attribute_type__data_type='DEC')),
            'count': 0,
        },
        'INT': {
            'initial': len(attributes.filter(attribute_type__data_type='INT')),
            'count': 0,
        },
        'JSON': {
            'initial': len(attributes.filter(attribute_type__data_type='JSON')),
            'count': 0,
        },
        'TXT': {
            'initial': len(attributes.filter(attribute_type__data_type='TXT')),
            'count': 0,
        },
        'FKEY': {
            'initial': len(attributes.filter(attribute_type__data_type__in=['FK-UUID', 'FK-INT'])),
            'count': 0,
        },
        'STR': {
            'initial': len(attributes.filter(attribute_type__data_type='STR')),
            'count': 0,
        },
    }

    att_count = len(attributes)
    print(f'\n\nStarting migration of {att_count} attribute records')  # noqa: T201

    for i, att in enumerate(attributes):
        dtype = att.attribute_type.data_type

        if dtype == 'DATE':
            new_val = AttributeValueDate(
                attribute_ptr=att,
                day=att.value_DATE_d,
                month=att.value_DATE_m,
                year=att.value_DATE_y,
                date=att.value_DATE,
                text=att.value_STR,
                creation_user=att.creation_user,
                modification_user=att.modification_user,
                creation_timestamp=att.creation_timestamp,
                modification_timestamp=att.modification_timestamp,
            )
            new_val.save_base(raw=True)

            stats[dtype]['count'] += 1

        elif dtype == 'DEC':
            new_val = AttributeValueDec(
                attribute_ptr=att,
                value=att.value_DEC,
                creation_user=att.creation_user,
                modification_user=att.modification_user,
                creation_timestamp=att.creation_timestamp,
                modification_timestamp=att.modification_timestamp,
            )
            new_val.save_base(raw=True)

            stats[dtype]['count'] += 1

        elif dtype == 'INT':
            new_val = AttributeValueInt(
                attribute_ptr=att,
                value=att.value_INT,
                creation_user=att.creation_user,
                modification_user=att.modification_user,
                creation_timestamp=att.creation_timestamp,
                modification_timestamp=att.modification_timestamp,
            )
            new_val.save_base(raw=True)

            stats[dtype]['count'] += 1

        elif dtype == 'JSON':
            new_val = AttributeValueJson(
                attribute_ptr=att,
                value=att.value_JSON,
                creation_user=att.creation_user,
                modification_user=att.modification_user,
                creation_timestamp=att.creation_timestamp,
                modification_timestamp=att.modification_timestamp,
            )
            new_val.save_base(raw=True)

            stats[dtype]['count'] += 1

        elif dtype == 'TXT':
            new_val = AttributeValueTxt(
                attribute_ptr=att,
                value=att.value_TXT,
                creation_user=att.creation_user,
                modification_user=att.modification_user,
                creation_timestamp=att.creation_timestamp,
                modification_timestamp=att.modification_timestamp,
            )
            new_val.save_base(raw=True)

            stats[dtype]['count'] += 1

        elif dtype == 'FK-UUID' or dtype == 'FK-INT':
            _id = att.value_JSON['id'] if dtype == 'FK-UUID' else int(att.value_JSON['id'])
            obj_class = att.value_JSON['class'].lower()
            obj_ct = ContentType.objects.get(app_label='dalme_app', model=obj_class.lower())

            new_val = AttributeValueFkey(
                attribute_ptr=att,
                target_content_type=obj_ct,
                target_id=_id,
                creation_user=att.creation_user,
                modification_user=att.modification_user,
                creation_timestamp=att.creation_timestamp,
                modification_timestamp=att.modification_timestamp,
            )
            new_val.save_base(raw=True)

            stats['FKEY']['count'] += 1

        elif dtype == 'STR':
            new_val = AttributeValueStr(
                attribute_ptr=att,
                value=att.value_STR,
                creation_user=att.creation_user,
                modification_user=att.modification_user,
                creation_timestamp=att.creation_timestamp,
                modification_timestamp=att.modification_timestamp,
            )
            new_val.save_base(raw=True)

            stats[dtype]['count'] += 1

        if i % 1000 == 0:
            print(f'{round(i*100/att_count)}% completed     ', end='\r', flush=True)  # noqa: T201

    print('Migration completed... \033[94m\033[1mOK\033[0m', end='\r', flush=True)  # noqa: T201
    print('Changing `FK-UUID` and `FK-INT` to `FKEY`...', end='')  # noqa: T201

    # update data types:
    for atype in AttributeType.objects.filter(data_type__in=['FK-UUID', 'FK-INT']):
        atype.data_type = 'FKEY'
        atype.modification_user = user_obj
        atype.save()

    print(' \033[94m\033[1mOK\033[0m')  # noqa: T201
    print('Verifying  stats:')  # noqa: T201

    total = 0
    for key, val in stats.items():
        total += val["count"]
        print(f'{key}: {val["initial"]} total, {val["count"]} migrated', end='')  # noqa: T201
        if val["initial"] == val["count"]:
            print(' \033[96m\033[1mOK\033[0m')  # noqa: T201
        else:
            print(' \033[93m\033[1mMISMATCH\033[0m')  # noqa: T201

    print(f'{att_count} attributes to migrate, {total} migrated')  # noqa: T201
    print('  Overall migration...', end='')  # noqa: T201


class Migration(migrations.Migration):  # noqa: D101
    atomic = False
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0008_data_m_misc'),
    ]

    operations = [
        migrations.RunPython(migrate_attributes),
    ]
