from django.conf import settings
from django.db import migrations


def create_attribute_options(apps, schema_editor):  # noqa: ARG001
    """Create options sets."""
    OptionsList = apps.get_model("dalme_app", "OptionsList")  # noqa: N806
    AttributeType = apps.get_model("dalme_app", "AttributeType")  # noqa: N806

    print('\n\nCreating options entryes for attributes...', end='')  # noqa: T201

    auth_list = OptionsList.objects.create(
        name='record authority',
        payload_type='static_list',
        description='List of authority sources for records.',
        payload=[
            {'label': 'Chancery', 'value': 'Chancery'},
            {'label': 'Church', 'value': 'Church'},
            {'label': 'Court', 'value': 'Court'},
            {'label': 'Notary', 'value': 'Notary'},
        ],
    )
    authority = AttributeType.objects.get(name='authority')
    authority.options = auth_list
    authority.save(update_fields=['options'])

    format_list = OptionsList.objects.create(
        name='record format',
        payload_type='static_list',
        description='List of formats for records.',
        payload=[
            {'label': 'Charter', 'value': 'Charter'},
            {'label': 'Register - demi-quarto', 'value': 'Register - demi-quarto'},
            {'label': 'Register - quarto', 'value': 'Register - quarto'},
        ],
    )
    att_format = AttributeType.objects.get(name='format')
    att_format.options = format_list
    att_format.save(update_fields=['options'])

    record_type_list = OptionsList.objects.create(
        name='record types',
        payload_type='static_list',
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
    record_type = AttributeType.objects.get(name='record_type')
    record_type.options = record_type_list
    record_type.save(update_fields=['options'])

    support_list = OptionsList.objects.create(
        name='record support',
        payload_type='static_list',
        description='List of support types for records.',
        payload=[
            {'label': 'Hybrid', 'value': 'Hybrid'},
            {'label': 'Paper', 'value': 'Paper'},
            {'label': 'Parchment', 'value': 'Parchment'},
            {'label': 'Vellum', 'value': 'Vellum'},
        ],
    )
    support = AttributeType.objects.get(name='support')
    support.options = support_list
    support.save(update_fields=['options'])

    rights_status_list = OptionsList.objects.create(
        name='rights status',
        payload_type='static_list',
        description='List of valid status values for rights policies.',
        payload=[
            {'label': 'Copyrighted', 'value': 'Copyrighted'},
            {'label': 'Orphaned', 'value': 'Orphaned'},
            {'label': 'Owned', 'value': 'Owned'},
            {'label': 'Public Domain', 'value': 'Public Domain'},
        ],
    )
    rights_status = AttributeType.objects.get(name='rights_status')
    rights_status.options = rights_status_list
    rights_status.save(update_fields=['options'])

    user_list = OptionsList.objects.create(
        name='full user list',
        payload_type='db_records',
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
    owner = AttributeType.objects.get(name='owner')
    owner.options = user_list
    owner.save(update_fields=['options'])

    rights_status_list = OptionsList.objects.create(
        name='rights status list',
        payload_type='field_choices',
        description='List of possible status values for rights policies.',
        payload={
            'app': 'dalme_app',
            'model': 'RightsPolicy',
            'choices': 'RIGHTS_STATUS',
        },
    )
    rights_status = AttributeType.objects.get(name='rights_status')
    rights_status.options = rights_status_list
    rights_status.save(update_fields=['options'])

    # type options for Publication

    # type options for Organization

    # type for Location?

    print(' \033[94m\033[1mOK\033[0m')  # noqa: T201
    print('  Overall migration...', end='')  # noqa: T201


class Migration(migrations.Migration):  # noqa: D101
    atomic = False
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0014_adj_and_remove_unused'),
    ]

    operations = [
        migrations.RunPython(create_attribute_options),
    ]
