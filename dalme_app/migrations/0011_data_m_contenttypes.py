from django.conf import settings
from django.db import migrations

CT_DATA = {
    'agent': {
        'name': 'Agent',
        'description': 'The direct performer or driver of an action (e.g. a person, an organization).',
        'atypes': [
            'id',
            'name',
            'type',
            'comments',
            'tags',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
        ],
    },
    'organization': {
        'name': 'Organization',
        'description': 'An organization such as a school, NGO, corporation, club, etc.',
        'parent': 'agent',
        'atypes': [
            'short_name',
            'url',
        ],
    },
    'person': {
        'name': 'Person',
        'description': 'A person (alive, dead, undead, or fictional).',
        'parent': 'agent',
        'atypes': ['social_status', 'religion', 'sex', 'legal_persona'],
    },
    'group': {
        'name': 'User Group',
        'description': 'A group of user accounts in the system.',
        'namespace': 'auth',
        'atypes': [],
    },
    'user': {
        'name': 'User Account',
        'description': "A person's account in the system.",
        'namespace': 'auth',
        'atypes': [
            'last_name',
            'first_name',
            'password',
            'last_login',
            'is_superuser',
            'username',
            'email',
            'is_staff',
            'is_active',
            'date_joined',
            'full_name',
            'groups',
        ],
    },
    'place': {
        'name': 'Place',
        'description': 'A physical or abstract location.',
        'atypes': [
            'id',
            'name',
            'comments',
            'tags',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
        ],
    },
    'location': {
        'name': 'Location',
        'description': 'A fixed, physical location.',
        'atypes': [
            'id',
            'type',
            'comments',
            'tags',
            'street_address',
            'postal_code',
            'pobox_number',
            'latitude',
            'longitude',
            'elevation',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
        ],
    },
    'countryreference': {
        'name': 'Country',
        'description': 'A country.',
        'parent': 'location',
        'atypes': [
            'id',
            'name',
            'alpha_3_code',
            'alpha_2_code',
            'num_code',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
        ],
    },
    'localereference': {
        'name': 'Locale',
        'description': 'A geographic place at which there is or was human activity',
        'parent': 'location',
        'atypes': [
            'id',
            'name',
            'administrative_region',
            'country',
            'latitude',
            'longitude',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
        ],
    },
    'languagereference': {
        'name': 'Language',
        'description': 'A structured system of communication that consists of grammar and vocabulary.',
        'atypes': [
            'id',
            'glottocode',
            'iso6393',
            'type',
            'parent',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
        ],
    },
    'collection': {
        'name': 'Collection',
        'description': 'A collection of items.',
        'atypes': [
            'id',
            'name',
            'description',
            'is_public',
            'owner',
            'permissions',
            'comments',
            'member_count',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
        ],
    },
    'rightspolicy': {
        'name': 'Rights Policy',
        'description': 'Guidelines and restrictions regulating the use of a resource.',
        'atypes': [
            'id',
            'name',
            'rights_status',
            'rights_notice',
            'licence',
            'rights',
            'rights_holder',
            'notice_display',
            'default_rights',
            'attachments',
            'comments',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
        ],
    },
    'recordgroup': {
        'name': 'Record Group',
        'description': "An organized unit (folder, volume, etc.) of documents grouped together either for current use or in the process of archival arrangement.",
        'atypes': [
            'id',
            'name',
            'short_name',
            'description',
            'parent',
            'type',
            'owner',
            'permissions',
            'comments',
            'tags',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
            'mk2_identifier',
            'mk1_identifier',
            'alt_identifier',
            'authority',
            'format',
            'support',
        ],
    },
    'publication': {
        'name': 'Publication',
        'description': "A written work of fiction or nonfiction.",
        'atypes': [
            'id',
            'name',
            'short_name',
            'description',
            'type',
            'zotero_key',
            'permissions',
            'comments',
            'tags',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
            'mk2_identifier',
            'mk1_identifier',
            'alt_identifier',
        ],
    },
    'record': {
        'name': 'Record',
        'description': "The smallest intellectually indivisible archival unit (e.g. a letter, memorandum, report, leaflet, or photograph). For example, a book or record album would be described as an item, but the individual chapters of the book or the discs or songs that make up the album would not be described as items.",
        'atypes': [
            'id',
            'name',
            'short_name',
            'description',
            'parent',
            'owner',
            'permissions',
            'comments',
            'tags',
            'creation_username',
            'creation_timestamp',
            'modification_username',
            'modification_timestamp',
            'mk2_identifier',
            'mk1_identifier',
            'alt_identifier',
            'archival_series',
            'archival_number',
            'date',
            'end_date',
            'start_date',
            'record_type',
            'record_type_phrase',
            'debt_phrase',
            'debt_amount',
            'debt_unit',
            'debt_unit_type',
            'debt_source',
            'has_inventory',
            'locale',
            'named_persons',
            'has_image',
            'collections',
            'no_folios',
            'has_pages',
            'is_public',
        ],
    },
}


def create_content_types_ext_dataset(apps, schema_editor):  # noqa: ARG001
    """Create data for content_type_ext table."""
    ContentType = apps.get_model('contenttypes', 'ContentType')  # noqa: N806
    ContentTypeExtended = apps.get_model("dalme_app", "ContentTypeExtended")  # noqa: N806
    AttributeType = apps.get_model('dalme_app', 'AttributeType')  # noqa: N806
    ContentAttributes = apps.get_model('dalme_app', 'ContentAttributes')  # noqa: N806
    User = apps.get_model("auth", "User")  # noqa: N806

    User.objects.get(pk=1)

    print('\n\nCreating `ContentTypeExtended` records:')  # noqa: T201

    for model, payload in CT_DATA.items():
        print(f'Processing model {model}', end='')  # noqa: T201
        app_label = payload.get('namespace', 'dalme_app')
        ctype = ContentType.objects.get(app_label=app_label, model=model)

        new_cte = ContentTypeExtended(
            contenttype_ptr=ctype,
            app_label=app_label,
            model=model,
            name=payload['name'],
            description=payload['description'],
            is_abstract=False,
        )
        new_cte.save_base(raw=True)

        if 'parent' in payload:
            parent = ContentTypeExtended.objects.get(model=payload['parent'])
            new_cte.parent = parent
            new_cte.save(update_fields=['parent'])

        if 'atypes' in payload:
            for at_name in payload['atypes']:
                at = AttributeType.objects.filter(short_name=at_name)
                if at.exists():
                    atype = at.first()
                    ContentAttributes.objects.create(content_type=new_cte, attribute_type=atype)

        print(' \033[94m\033[1mOK\033[0m')  # noqa: T201

    print('  Overall migration...', end='')  # noqa: T201


class Migration(migrations.Migration):  # noqa: D101
    atomic = False
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0010_data_m_basic_types'),
    ]

    operations = [
        migrations.RunPython(create_content_types_ext_dataset),
    ]
