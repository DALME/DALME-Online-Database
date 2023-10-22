from django.conf import settings
from django.db import migrations
from django.db.models import Q


def add_libraries(apps, schema_editor):  # noqa: ARG001
    """Add library instances to new model."""
    LibraryReference = apps.get_model("dalme_app", "LibraryReference")  # noqa: N806
    User = apps.get_model("auth", "User")  # noqa: N806

    user_obj = User.objects.get(pk=1)

    print('\n\nCreating new library records...', end='')  # noqa: T201

    LibraryReference.objects.create(
        zotero_id=2205678,
        name='DALME',
        description='Documentary Archaeology of Late Medieval Europe',
        editions_id='A4QHN348',
        creation_user=user_obj,
        modification_user=user_obj,
    )

    LibraryReference.objects.create(
        zotero_id=4927659,
        name='GP',
        description='Global Pharmacopeias',
        editions_id='UZJGXUF2',
        creation_user=user_obj,
        modification_user=user_obj,
    )

    print(' \033[94m\033[1mOK\033[0m')  # noqa: T201


def create_attribute_type(apps, schema_editor):  # noqa: ARG001
    """Creates `library` attribute type."""
    AttributeType = apps.get_model("dalme_app", "Attribute_type")  # noqa: N806
    User = apps.get_model("auth", "User")  # noqa: N806
    
    user_obj = User.objects.get(pk=1)

    print('\n\nCreating new attribute type...', end='')  # noqa: T201

    AttributeType.objects.create(
        name='Library',
        short_name='library',
        description='A reference to a specific Zotero library or collection.',
        data_type='FK-INT',
        source='DALME',
        options_list="[{'label': i.name+' ('+i.description+')', 'value': i.id} for i in LibraryReference.objects.all().order_by('name')]",
        creation_user=user_obj,
        modification_user=user_obj,
    )

    print(' \033[94m\033[1mOK\033[0m')  # noqa: T201


def add_to_existing(apps, schema_editor):  # noqa: ARG001
    """Add new attribute to existing records of `bibliography` type."""
    AttributeType = apps.get_model("dalme_app", "Attribute_type")  # noqa: N806
    Attribute = apps.get_model('dalme_app', 'Attribute')  # noqa: N806
    ContentType = apps.get_model('contenttypes', 'ContentType')  # noqa: N806
    LibraryReference = apps.get_model("dalme_app", "LibraryReference")  # noqa: N806
    Set = apps.get_model("dalme_app", "Set")  # noqa: N806
    Source = apps.get_model("dalme_app", "Source")  # noqa: N806
    User = apps.get_model("auth", "User")  # noqa: N806

    user_obj = User.objects.get(pk=1)
    library_atype = AttributeType.objects.get(short_name='library')
    dalme_lib = {
        'id': LibraryReference.objects.get(name='DALME').id,
        'class': 'LibraryReference'
        }
    pharma_lib = {
        'id': LibraryReference.objects.get(name='GP').id,
        'class': 'LibraryReference'
        }
    pharma_dataset = Set.objects.get(name='Team Pharmacopeia Sources')
    source_ctype = ContentType.objects.get(app_label='dalme_app', model='Source')
    sources = Source.objects.filter(Q(type__in=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]))
    record_count = len(sources)

    print(f'\n\nStarting processing of {record_count} records')  # noqa: T201

    for i, source in enumerate(sources):
        lib_value = pharma_lib if source.primary_dataset.id == pharma_dataset.id else dalme_lib
        new_val = Attribute(
            content_type=source_ctype,
            object_id=source.id,
            attribute_type=library_atype,
            value_JSON=lib_value,
            creation_user=user_obj,
            modification_user=user_obj,
            )
        new_val.save()
        
        if i % 10 == 0:
            print(f'{round(i*100/record_count)}% completed     ', end='\r', flush=True)  # noqa: T201

    print('\nMigration completed... \033[94m\033[1mOK\033[0m', end='\r', flush=True)  # noqa: T201


class Migration(migrations.Migration):  # noqa: D101
    atomic = False
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0007_libraryreference'),
    ]

    operations = [
        migrations.RunPython(add_libraries),
        migrations.RunPython(create_attribute_type),
        migrations.RunPython(add_to_existing),
    ]