from contextlib import suppress

from django.conf import settings
from django.db import migrations


def create_attribute_options(apps, schema_editor):  # noqa: ARG001
    """Create options sets."""
    OptionsList = apps.get_model("dalme_app", "OptionsList")  # noqa: N806
    AttributeType = apps.get_model("dalme_app", "AttributeType")  # noqa: N806

    auth_list = OptionsList.objects.create(
        name='record authority',
        type='static_list',
        description='List of authority sources for records.',
        payload=[
            {'label': 'Chancery', 'value': 'Chancery'},
            {'label': 'Church', 'value': 'Church'},
            {'label': 'Court', 'value': 'Court'},
            {'label': 'Notary', 'value': 'Notary'},
        ],
    )
    authority = AttributeType.objects.get(short_name='authority')
    authority.options = auth_list
    authority.save(update_fields=['options'])

    format_list = OptionsList.objects.create(
        name='record format',
        type='static_list',
        description='List of formats for records.',
        payload=[
            {'label': 'Charter', 'value': 'Charter'},
            {'label': 'Register - demi-quarto', 'value': 'Register - demi-quarto'},
            {'label': 'Register - quarto', 'value': 'Register - quarto'},
        ],
    )
    att_format = AttributeType.objects.get(short_name='format')
    att_format.options = format_list
    att_format.save(update_fields=['options'])

    record_type_list = OptionsList.objects.create(
        name='record types',
        type='static_list',
        description='List of record types.',
        payload=[
            {'label': 'Inventory-Comanda', 'value': 'Inventory-Comanda', 'group': 'Inventory'},
            {'label': 'Inventory-Criminal Inquest', 'value': 'Inventory-Criminal Inquest', 'group': 'Inventory'},
            {'label': 'Inventory-Custody', 'value': 'Inventory-Custody', 'group': 'Inventory'},
            {'label': 'Inventory-Division', 'value': 'Inventory-Division', 'group': 'Inventory'},
            {'label': 'Inventory-Donation', 'value': 'Inventory-Donation', 'group': 'Inventory'},
            {'label': 'Inventory-Dowry', 'value': 'Inventory-Dowry', 'group': 'Inventory'},
            {'label': 'Inventory-Dowry Restitution', 'value': 'Inventory-Dowry Restitution', 'group': 'Inventory'},
            {'label': 'Inventory-Ecclesiastical', 'value': 'Inventory-Ecclesiastical', 'group': 'Inventory'},
            {'label': 'Inventory-Emancipation', 'value': 'Inventory-Emancipation', 'group': 'Inventory'},
            {'label': 'Inventory-Generic', 'value': 'Inventory-Generic', 'group': 'Inventory'},
            {'label': 'Inventory-Guardianship', 'value': 'Inventory-Guardianship', 'group': 'Inventory'},
            {'label': 'Inventory-Insolvency', 'value': 'Inventory-Insolvency', 'group': 'Inventory'},
            {'label': 'Inventory-Legacy', 'value': 'Inventory-Legacy', 'group': 'Inventory'},
            {'label': 'Inventory-List of objects', 'value': 'Inventory-List of objects', 'group': 'Inventory'},
            {'label': 'Inventory-Postmortem', 'value': 'Inventory-Postmortem', 'group': 'Inventory'},
            {'label': 'Inventory-Premortem', 'value': 'Inventory-Premortem', 'group': 'Inventory'},
            {'label': 'Inventory-Probate', 'value': 'Inventory-Probate', 'group': 'Inventory'},
            {'label': 'Inventory-Quittance', 'value': 'Inventory-Quittance', 'group': 'Inventory'},
            {
                'label': 'Inventory-Repudiation of inheritance',
                'value': 'Inventory-Repudiation of inheritance',
                'group': 'Inventory',
            },
            {
                'label': 'Inventory-Restitution of pawned goods',
                'value': 'Inventory-Restitution of pawned goods',
                'group': 'Inventory',
            },
            {'label': 'Inventory-Ship', 'value': 'Inventory-Ship', 'group': 'Inventory'},
            {
                'label': 'Inventory-Taking up inheritance',
                'value': 'Inventory-Taking up inheritance',
                'group': 'Inventory',
            },
            {'label': 'Inventory-Tax seizure', 'value': 'Inventory-Tax seizure', 'group': 'Inventory'},
            {'label': 'Inventory-Undefended Goods', 'value': 'Inventory-Undefended Goods', 'group': 'Inventory'},
            {'label': 'Account Book-Household', 'value': 'Account Book-Household', 'group': 'Account Book'},
            {'label': 'Account Book-Commercial', 'value': 'Account Book-Commercial', 'group': 'Account Book'},
            {'label': 'Account Book-Ecclesiastical', 'value': 'Account Book-Ecclesiastical', 'group': 'Account Book'},
            {'label': 'Account Book-Other', 'value': 'Account Book-Other', 'group': 'Account Book'},
            {'label': 'Guardianship', 'value': 'Guardianship', 'group': 'Guardianship'},
            {'label': 'Liquidation of guardianship', 'value': 'Liquidation of guardianship', 'group': 'Guardianship'},
            {'label': 'Failed Seizure', 'value': 'Failed Seizure', 'group': 'Seizure'},
            {'label': 'Seizure', 'value': 'Seizure', 'group': 'Seizure'},
            {'label': 'Seizure-Debt', 'value': 'Seizure-Debt', 'group': 'Seizure'},
            {'label': 'Seizure-Confiscation', 'value': 'Seizure-Confiscation', 'group': 'Seizure'},
            {'label': 'Testament', 'value': 'Testament', 'group': 'Testament'},
            {'label': 'Testamentary execution', 'value': 'Testamentary execution', 'group': 'Testament'},
            {'label': 'Sale-Auction', 'value': 'Sale-Auction', 'group': 'Sales'},
            {'label': 'Sale-Notarial', 'value': 'Sale-Notarial', 'group': 'Sales'},
            {'label': 'Sale-Account', 'value': 'Sale-Account', 'group': 'Sales'},
            {'label': 'Estimate-Dowry', 'value': 'Estimate-Dowry', 'group': 'Estimates'},
            {'label': 'Estimate-Testament', 'value': 'Estimate-Testament', 'group': 'Estimates'},
            {'label': 'Estimate-Insolvency', 'value': 'Estimate-Insolvency', 'group': 'Estimates'},
            {'label': 'Estimate-Pledge', 'value': 'Estimate-Pledge', 'group': 'Estimates'},
            {'label': 'Estimate-Investment', 'value': 'Estimate-Investment', 'group': 'Estimates'},
            {'label': 'Estimate-Theft', 'value': 'Estimate-Theft', 'group': 'Estimates'},
            {'label': 'Tariffs-Price Caps', 'value': 'Tariffs-Price Caps', 'group': 'Tariffs'},
            {'label': 'Tariffs-Lists', 'value': 'Tariffs-Lists', 'group': 'Tariffs'},
            {'label': 'Tariffs-Customs Registers', 'value': 'Tariffs-Customs Registers', 'group': 'Tariffs'},
            {'label': 'Arrest', 'value': 'Arrest', 'group': 'Other'},
            {'label': 'Auction', 'value': 'Auction', 'group': 'Other'},
            {'label': 'Codicil', 'value': 'Codicil', 'group': 'Other'},
            {'label': 'Eviction', 'value': 'Eviction', 'group': 'Other'},
            {'label': 'Incarceration', 'value': 'Incarceration', 'group': 'Other'},
            {'label': 'Object List-Fictional', 'value': 'Object List-Fictional', 'group': 'Other'},
            {'label': 'Order to deliver goods', 'value': 'Order to deliver goods', 'group': 'Other'},
            {'label': 'Promise to pay debt', 'value': 'Promise to pay debt', 'group': 'Other'},
            {'label': 'Renvoi', 'value': 'Renvoi', 'group': 'Other'},
            {'label': 'unclear', 'value': 'unclear', 'group': 'Other'},
        ],
    )
    record_type = AttributeType.objects.get(short_name='record_type')
    record_type.options = record_type_list
    record_type.save(update_fields=['options'])

    support_list = OptionsList.objects.create(
        name='record support',
        type='static_list',
        description='List of support types for records.',
        payload=[
            {'label': 'Hybrid', 'value': 'Hybrid'},
            {'label': 'Paper', 'value': 'Paper'},
            {'label': 'Parchment', 'value': 'Parchment'},
            {'label': 'Vellum', 'value': 'Vellum'},
        ],
    )
    support = AttributeType.objects.get(short_name='support')
    support.options = support_list
    support.save(update_fields=['options'])

    rights_status_list = OptionsList.objects.create(
        name='rights status',
        type='static_list',
        description='List of valid status values for rights policies.',
        payload=[
            {'label': 'Copyrighted', 'value': 'Copyrighted'},
            {'label': 'Orphaned', 'value': 'Orphaned'},
            {'label': 'Owned', 'value': 'Owned'},
            {'label': 'Public Domain', 'value': 'Public Domain'},
        ],
    )
    rights_status = AttributeType.objects.get(short_name='rights_status')
    rights_status.options = rights_status_list
    rights_status.save(update_fields=['options'])

    user_list = OptionsList.objects.create(
        name='full user list',
        type='db_records',
        description='Full list of active system users.',
        payload={
            'app': 'auth',
            'model': 'User',
            'filters': {'is_active': True},
            'concordance': {
                'label': 'profile.full_name',
                'value': 'id',
                'detail': 'username',
            },
        },
    )
    owner = AttributeType.objects.get(short_name='owner')
    owner.options = user_list
    owner.save(update_fields=['options'])

    rights_status_list = OptionsList.objects.create(
        name='rights status list',
        type='field_choices',
        description='List of possible status values for rights policies.',
        payload={
            'app': 'dalme_app',
            'model': 'RightsPolicy',
            'choices': 'RIGHTS_STATUS',
        },
    )
    rights_status = AttributeType.objects.get(short_name='rights_status')
    rights_status.options = rights_status_list
    rights_status.save(update_fields=['options'])


def fix_attribute_types(apps, schema_editor):  # noqa: ARG001
    """Fix attribute types."""
    AttributeType = apps.get_model("dalme_app", "AttributeType")  # noqa: N806

    renames = {
        'creation_username': 'creation_user',
        'modification_username': 'modification_user',
        'is_public': 'is_published',
        'required': 'is_required',
        'options_list': 'options',
    }
    to_fkey = [
        'owner',
        'parent',
        'creation_username',
        'modification_username',
        'type',
        'same_as',
        'last_user',
        'is_public',
    ]
    to_bool = [
        'has_inventory',
        'is_superuser',
        'is_staff',
        'is_active',
        'has_image',
        'required',
        'has_pages',
        'help_flag',
        'has_landing',
        'notice_display',
    ]
    to_int = ['rights_status']
    to_rrel = [
        'comments',
        'named_persons',
        'collections',
        'attribute_types',
        'permissions',
        'groups',
        'tags',
        'attachments',
    ]
    to_json = ['options_list']

    to_local = [
        'id',
        'creation_user',
        'modification_user',
        'creation_timestamp',
        'modification_timestamp',
        'owner',
        'type',
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
        'subject',
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
        'latitude',
        'longitude',
        'has_image',
        'no_folios',
        'same_as',
        'options',
        'has_pages',
        'help_flag',
        'member_count',
        'is_required',
    ]

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

    for at_name in to_json:
        at = AttributeType.objects.get(short_name=at_name)
        at.data_type = 'JSON'
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


class Migration(migrations.Migration):  # noqa: D101
    atomic = False
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0010_data_m_attributes'),
    ]

    operations = [
        migrations.RunPython(create_attribute_options),
        migrations.RunPython(fix_attribute_types),
    ]
