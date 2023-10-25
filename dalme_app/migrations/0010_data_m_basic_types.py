from django.conf import settings
from django.db import migrations


def migrate_agents(apps, schema_editor):
    """Split Agents into Org and Person."""
    Agent = apps.get_model('dalme_app', 'Agent')  # noqa: N806
    Person = apps.get_model('dalme_app', 'Person')  # noqa: N806

    print('\n\nSplitting Agent records...', end='')  # noqa: T201

    for agent in Agent.objects.all():
        if agent.agent_type == 1:
            new_rec = Person(
                agent_ptr=agent,
                user=agent.old_user,
                agent_type=1,
                creation_user=agent.creation_user,
                modification_user=agent.modification_user,
                creation_timestamp=agent.creation_timestamp,
                modification_timestamp=agent.modification_timestamp,
            )
            new_rec.save_base(raw=True)

    print(' \033[94m\033[1mOK\033[0m')  # noqa: T201


def migrate_places(apps, schema_editor):
    """Update places."""
    ContentType = apps.get_model('contenttypes', 'ContentType')  # noqa: N806
    Place = apps.get_model('dalme_app', 'Place')  # noqa: N806
    Location = apps.get_model('dalme_app', 'Location')  # noqa: N806
    AttributeType = apps.get_model('dalme_app', 'AttributeType')  # noqa: N806
    AttributeValueFkey = apps.get_model('dalme_app', 'AttributeValueFkey')  # noqa: N806

    locale_atype = AttributeType.objects.get(short_name='locale')
    locale_ctype = ContentType.objects.get(app_label='dalme_app', model='localereference')
    location_ctype = ContentType.objects.get(app_label='dalme_app', model='location')

    print('Fixing Place records...', end='')  # noqa: T201

    for place in Place.objects.all():
        if place.locale:
            new_loc = Location(
                location_type=4,
                creation_user=place.creation_user,
                modification_user=place.modification_user,
                creation_timestamp=place.creation_timestamp,
                modification_timestamp=place.modification_timestamp,
            )
            new_loc.save()

            place.location = new_loc
            place.save(update_fields=['location'])

            new_att = AttributeValueFkey(
                content_type=location_ctype,
                object_id=new_loc.id,
                attribute_type=locale_atype,
                target_content_type=locale_ctype,
                target_id=place.locale.id,
                creation_user=place.creation_user,
                modification_user=place.modification_user,
                creation_timestamp=place.creation_timestamp,
                modification_timestamp=place.modification_timestamp,
            )
            new_att.save()

    print(' \033[94m\033[1mOK\033[0m')  # noqa: T201


def migrate_archives(apps, schema_editor):
    """Make archives into orgs."""
    ContentType = apps.get_model('contenttypes', 'ContentType')  # noqa: N806
    Record = apps.get_model('dalme_app', 'Record')  # noqa: N806
    Organization = apps.get_model('dalme_app', 'Organization')  # noqa: N806
    Attribute = apps.get_model('dalme_app', 'Attribute')  # noqa: N806

    org_ctype = ContentType.objects.get(app_label='dalme_app', model='organization')
    record_ctype = ContentType.objects.get(app_label='dalme_app', model='record')

    print('Converting `Source > Archive` records into `Organization` records...', end='')  # noqa: T201
    count = 0

    for record in Record.objects.filter(type=19):
        # create org
        new_org = Organization(
            id=record.id,
            name=record.name,
            agent_type=2,
            short_name=record.short_name,
            creation_user=record.creation_user,
            modification_user=record.modification_user,
            creation_timestamp=record.creation_timestamp,
            modification_timestamp=record.modification_timestamp,
        )
        new_org.save()

        # fix attributes
        for att in Attribute.objects.filter(content_type=record_ctype, object_id=record.id):
            att.content_type = org_ctype
            att.save(update_fields=['content_type'])

        # fix children
        for child in Record.objects.filter(old_parent=record.id):
            child.parent_type = org_ctype
            child.parent_id = new_org.id
            child.save(update_fields=['parent_type', 'parent_id'])

        # remove source record
        record.delete()
        count += 1

    print(' \033[94m\033[1mOK\033[0m')  # noqa: T201
    print(f'{count} records converted')  # noqa: T201


def migrate_biblio_sources(apps, schema_editor):
    """Move biblio sources to publications."""
    ContentType = apps.get_model('contenttypes', 'ContentType')  # noqa: N806
    Record = apps.get_model('dalme_app', 'Record')  # noqa: N806
    Publication = apps.get_model('dalme_app', 'Publication')  # noqa: N806
    Attribute = apps.get_model('dalme_app', 'Attribute')  # noqa: N806

    pub_ctype = ContentType.objects.get(app_label='dalme_app', model='publication')
    record_ctype = ContentType.objects.get(app_label='dalme_app', model='record')

    print('Converting `Source > Bibliography` records into `Publication` records...', end='')  # noqa: T201
    count = 0

    for record in Record.objects.filter(type__in=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]):
        # create publication
        new_pub = Publication(
            id=record.id,
            name=record.name,
            short_name=record.short_name,
            creation_user=record.creation_user,
            modification_user=record.modification_user,
            creation_timestamp=record.creation_timestamp,
            modification_timestamp=record.modification_timestamp,
        )
        new_pub.save()

        # fix attributes
        for att in Attribute.objects.filter(content_type=record_ctype, object_id=record.id):
            att.content_type = pub_ctype
            att.save(update_fields=['content_type'])

        # fix children
        for child in Record.objects.filter(old_parent=record.id):
            child.parent_type = pub_ctype
            child.parent_id = new_pub.id
            child.save(update_fields=['parent_type', 'parent_id'])

        # remove source record
        record.delete()
        count += 1

    print(' \033[94m\033[1mOK\033[0m')  # noqa: T201
    print(f'{count} records converted')  # noqa: T201


def migrate_archival_files(apps, schema_editor):
    """Move archival files to record groups."""
    ContentType = apps.get_model('contenttypes', 'ContentType')  # noqa: N806
    Record = apps.get_model('dalme_app', 'Record')  # noqa: N806
    RecordGroup = apps.get_model('dalme_app', 'RecordGroup')  # noqa: N806
    Attribute = apps.get_model('dalme_app', 'Attribute')  # noqa: N806

    rg_ctype = ContentType.objects.get(app_label='dalme_app', model='recordgroup')
    record_ctype = ContentType.objects.get(app_label='dalme_app', model='record')

    print('Converting `Source > Archival File` records into `RecordGroup` records...', end='')  # noqa: T201
    count = 0

    for record in Record.objects.filter(type=12):
        # create record group
        new_rg = RecordGroup(
            id=record.id,
            name=record.name,
            short_name=record.short_name,
            creation_user=record.creation_user,
            modification_user=record.modification_user,
            creation_timestamp=record.creation_timestamp,
            modification_timestamp=record.modification_timestamp,
        )
        new_rg.save()

        # add parent, if any
        if record.parent_type:
            new_rg.parent_type = record.parent_type
            new_rg.parent_id = record.parent_id
            new_rg.save(update_fields=['parent_type', 'parent_id'])
        elif record.old_parent:
            pt = ContentType.objects.get_for_model(record.old_parent)
            new_rg.parent_type = pt
            new_rg.parent_id = record.parent.id
            new_rg.save(update_fields=['parent_type', 'parent_id'])

        # fix attributes
        for att in Attribute.objects.filter(content_type=record_ctype, object_id=record.id):
            att.content_type = rg_ctype
            att.save(update_fields=['content_type'])

        # fix children
        for child in Record.objects.filter(old_parent=record.id):
            child.parent_type = rg_ctype
            child.parent_id = new_rg.id
            child.save(update_fields=['parent_type', 'parent_id'])

        # remove source record
        record.delete()
        count += 1

    print(' \033[94m\033[1mOK\033[0m')  # noqa: T201
    print(f'{count} records converted')  # noqa: T201
    print('  Overall migration...', end='')  # noqa: T201


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0009_data_m_attributes'),
    ]

    operations = [
        migrations.RunPython(migrate_agents),
        migrations.RunPython(migrate_places),
        migrations.RunPython(migrate_archives),
        migrations.RunPython(migrate_biblio_sources),
        migrations.RunPython(migrate_archival_files),
    ]
