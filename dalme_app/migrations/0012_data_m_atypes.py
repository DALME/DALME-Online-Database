from contextlib import suppress

from django.conf import settings
from django.db import migrations


def fix_attribute_types(apps, schema_editor):
    """Fix attribute types."""
    AttributeType = apps.get_model('dalme_app', 'AttributeType')  # noqa: N806

    renames = {
        'creation_username': 'creation_user',
        'modification_username': 'modification_user',
        'is_public': 'is_published',
    }

    to_fkey = [
        'owner',
        'parent',
        'creation_username',
        'modification_username',
        'type',
        'same_as',
    ]
    to_bool = [
        'has_inventory',
        'is_superuser',
        'is_staff',
        'is_active',
        'has_image',
        'has_pages',
        'help_flag',
        'notice_display',
        'is_public',
    ]
    to_int = ['rights_status']
    to_rrel = [
        'comments',
        'named_persons',
        'collections',
        'permissions',
        'groups',
        'tags',
        'attachments',
    ]

    to_local = [
        'id',
        'creation_username',
        'modification_username',
        'creation_timestamp',
        'modification_timestamp',
        'owner',
        'name',
        'short_name',
        'password',
        'last_login',
        'is_superuser',
        'username',
        'email',
        'is_staff',
        'is_active',
        'date_joined',
        'full_name',
        'file_size',
        'required',
        'glottocode',
        'iso6393',
        'alpha_3_code',
        'alpha_2_code',
        'num_code',
        'administrative_region',
        'file',
        'last_modified',
        'last_user',
        'rights_status',
        'rights_notice',
        'licence',
        'rights',
        'rights_holder',
        'notice_display',
        'default_rights',
        'last_name',
        'first_name',
        'has_image',
        'no_folios',
        'same_as',
        'has_pages',
        'help_flag',
        'member_count',
    ]

    print('\n\nApplying fixes to `AttributeType` records...', end='')  # noqa: T201

    for at_name in to_fkey:
        at = AttributeType.objects.get(short_name=at_name)
        at.data_type = 'FKEY'
        at.save(update_fields=['data_type'])

    for at_name in to_bool:
        at = AttributeType.objects.get(short_name=at_name)
        at.data_type = 'BOOL'
        at.save(update_fields=['data_type'])

    for at_name in to_int:
        at = AttributeType.objects.get(short_name=at_name)
        at.data_type = 'INT'
        at.save(update_fields=['data_type'])

    for at_name in to_rrel:
        at = AttributeType.objects.get(short_name=at_name)
        at.data_type = 'RREL'
        at.save(update_fields=['data_type'])

    for old, new in renames.items():
        at = AttributeType.objects.get(short_name=old)
        at.short_name = new
        at.save(update_fields=['short_name'])

    for at_name in to_local:
        with suppress(Exception):
            at = AttributeType.objects.get(short_name=at_name)
            at.is_local = True
            at.save(update_fields=['is_local'])

    print(' \033[94m\033[1mOK\033[0m')  # noqa: T201


def clean_up_attribute_types(apps, schema_editor):
    """Remove unused attribute types."""
    ContentAttributes = apps.get_model('dalme_app', 'ContentAttributes')  # noqa: N806
    AttributeType = apps.get_model('dalme_app', 'AttributeType')  # noqa: N806
    Attribute = apps.get_model('dalme_app', 'Attribute')  # noqa: N806

    used_types_ct = list({entry.attribute_type.id for entry in ContentAttributes.objects.all()})
    used_types_att = list({att.attribute_type.id for att in Attribute.objects.all()})

    print('Reviewing `AttributeTypes`:')  # noqa: T201

    if len(used_types_ct) != len(used_types_att):
        if len(used_types_ct) > len(used_types_att):
            diff = [i for i in used_types_ct if i not in used_types_att]
        else:
            diff = [i for i in used_types_att if i not in used_types_ct]
    else:
        diff = []

    print(f'{len(used_types_ct)} attribute types are currently in use per CT count.')  # noqa: T201
    print(f'{len(used_types_att)} attribute types are currently in use per ATT count.')  # noqa: T201

    if len(diff) > 0:
        print(  # noqa: T201
            f'The extra types are: {", ".join([AttributeType.objects.get(pk=i).short_name for i in diff])}.',
        )

    used_types = list(set(used_types_ct + used_types_att))
    count = 0
    removed = []
    print('Removing unused types...', end='')  # noqa: T201

    for atype in AttributeType.objects.all():
        if atype.id not in used_types and not atype.is_local and atype.data_type != 'RREL':
            removed.append(atype.short_name)
            atype.delete()
            count += 1

    print(' \033[94m\033[1mOK\033[0m')  # noqa: T201
    print(f'{count} attribute types removed from DB.')  # noqa: T201
    print(', '.join(removed))  # noqa: T201
    print('  Overall migration...', end='')  # noqa: T201


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0011_data_m_contenttypes'),
    ]

    operations = [
        migrations.RunPython(fix_attribute_types),
        migrations.RunPython(clean_up_attribute_types),
    ]
