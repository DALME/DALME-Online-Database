from django.conf import settings
from django.contrib.contenttypes.management import create_contenttypes
from django.db import migrations


def update_content_types(apps, schema_editor):  # noqa: ARG001, C901
    """Update content types."""
    app_config = apps.get_app_config('dalme_app')
    app_config.models_module = True
    print('\n')  # noqa: T201
    create_contenttypes(app_config)

    ContentType = apps.get_model('contenttypes', 'ContentType')  # noqa: N806
    ContentTypeExtended = apps.get_model("dalme_app", "ContentTypeExtended")  # noqa: N806
    User = apps.get_model("auth", "User")  # noqa: N806

    new_ct_extended = [
        {
            'name': 'Source',
            'short_name': 'source',
            'description': 'A place, person, or thing from which something originates or can be obtained (e.g. an archive, a publication, etc).',
        },
        {
            'name': 'Agent',
            'short_name': 'agent',
            'description': 'The direct performer or driver of an action (e.g. a person, an organization).',
        },
        {
            'name': 'Place',
            'short_name': 'place',
            'description': 'A location, an entity with a somewhat fixed, physical extension.',
        },
        {
            'name': 'Collection',
            'short_name': 'collection',
            'description': 'A collection of items.',
        },
        {
            'name': 'User Account',
            'short_name': 'user',
            'description': "A person's account in the system.",
            'namespace': 'auth',
        },
        {
            'name': 'Group',
            'short_name': 'group',
            'description': "A group of user accounts in the system.",
            'namespace': 'auth',
        },
        {
            'name': 'Page',
            'short_name': 'page',
            'description': 'One side of a leaf (a sheet or half-sheet) of paper, parchment, or other material.',
        },
        {
            'name': 'Object',
            'short_name': 'object',
            'description': 'A material thing.',
        },
        {
            'name': 'Concept',
            'short_name': 'concept',
            'description': 'Refers to records that represent concepts (e.g. entries in the ATT).',
        },
        {
            'name': 'Transcription',
            'short_name': 'transcription',
            'description': 'A standardized representation of a text or other source.',
        },
        {
            'name': 'Wordform',
            'short_name': 'wordform',
            'description': 'One of the representations of a lexeme.',
        },
        {
            'name': 'Token',
            'short_name': 'token',
            'description': 'A string representation of a word as it appears in a document.',
        },
        {
            'name': 'Headword',
            'short_name': 'headword',
            'description': 'A standardized representation of a lemma.',
        },
        {
            'name': 'Language',
            'short_name': 'languagereference',
            'description': 'A structured system of communication that consists of grammar and vocabulary.',
        },
        {
            'name': 'Locale',
            'short_name': 'localereference',
            'description': 'A geographic place at which there is or was human activity.',
        },
        {
            'name': 'Rights Policy',
            'short_name': 'rightspolicy',
            'description': 'Guidelines and restrictions regulating the use of a resource.',
        },
        {
            'name': 'Entity Phrase',
            'short_name': 'entityphrase',
            'description': 'A portion of a text that identifies an entity (directly or not).',
        },
    ]

    user_obj = User.objects.get(pk=1)

    for ct in new_ct_extended:
        app_label = ct.get('namespace', 'dalme_app')
        ct_object = ContentType.objects.get(app_label=app_label, model=ct['short_name'])
        ContentTypeExtended.objects.create(
            name=ct['name'],
            short_name=ct['short_name'],
            description=ct['description'],
            content_type=ct_object,
            creation_user=user_obj,
            modification_user=user_obj,
        )

    # + country (18) to CountryReference (190)
    country_dct = ContentType.objects.get(pk=190)
    country_cte = ContentTypeExtended.objects.get(pk=18)
    country_cte.content_type = country_dct
    country_cte.save(update_fields=['content_type'])

    # create parent records
    agents = [15, 16]
    places = [34, 17, 18]
    sources = [1, 2, 3, 6, 7, 8, 9, 10, 11, 19]
    books = [4, 5]
    archives = [12]
    files = [13]

    for ct in ContentTypeExtended.objects.all():
        parents = []
        if ct.id in agents:
            parents.append(ContentTypeExtended.objects.get(short_name='agent').id)
        elif ct.id in places:
            parents.append(ContentTypeExtended.objects.get(short_name='place').id)
        elif ct.id in sources:
            parents.append(ContentTypeExtended.objects.get(short_name='source').id)
        elif ct.id in books:
            parents.append(ContentTypeExtended.objects.get(short_name='book').id)
        elif ct.id in archives:
            parents.append(ContentTypeExtended.objects.get(short_name='archive').id)
        elif ct.id in files:
            parents.append(ContentTypeExtended.objects.get(short_name='file_unit').id)

        if len(parents) > 0:
            for p_id in parents:
                if p_id:
                    ct.parents_list.add(ContentTypeExtended.objects.get(pk=p_id))

        ct.is_abstract = ct.content_type is None
        ct.save(update_fields=['is_abstract'])


class Migration(migrations.Migration):  # noqa: D101
    atomic = False
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0006_sql_casts'),
    ]

    operations = [
        migrations.RunPython(update_content_types),
    ]
