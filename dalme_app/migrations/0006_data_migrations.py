from django.conf import settings
from django.contrib.contenttypes.management import create_contenttypes
from django.db import migrations


def update_content_types(apps, schema_editor):  # noqa: ARG001
    """Update content types."""
    app_config = apps.get_app_config('dalme_app')
    app_config.models_module = True
    create_contenttypes(app_config)

    ContentType = apps.get_model('contenttypes', 'ContentType')  # noqa: N806
    ContentTypeExtended = apps.get_model("dalme_app", "ContentTypeExtended")  # noqa: N806

    coll_dct = ContentType.objects.get(app_label='dalme_app', model='collection')
    new_ct_extended = [
        {
            'name': 'Source',
            'short_name': 'source',
            'description': 'A place, person, or thing from which something originates or can be obtained (e.g. an archive, a publication, etc).',
            'dct_id': 125,
        },
        {
            'name': 'Agent',
            'short_name': 'agent',
            'description': 'The direct performer or driver of an action (e.g. a person, an organization).',
            'dct_id': 104,
        },
        {
            'name': 'Place',
            'short_name': 'place',
            'description': 'A location, an entity with a somewhat fixed, physical extension.',
            'dct_id': 115,
        },
        {
            'name': 'Collection',
            'short_name': 'collection',
            'description': 'A collection of items.',
            'dct_id': coll_dct.id,
        },
    ]

    for ct in new_ct_extended:
        ct_object = ContentType.objects.get(pk=ct['dct_id'])
        ContentTypeExtended.objects.create(
            name=ct['name'],
            short_name=ct['short_name'],
            description=ct['description'],
            content_type=ct_object,
        )

    # + country (18) to CountryReference (190)
    country_dct = ContentType.objects.get(pk=190)
    country_cte = ContentTypeExtended.objects.get(pk=18)
    country_cte.content_type = country_dct
    country_cte.save()

    # create parent records
    agents = [14, 15]
    places = [16, 17, 18]
    for ct in ContentTypeExtended.objects.all():
        if ct.short_name == 'collection':
            continue

        if ct.id in agents:
            parents = [ContentTypeExtended.objects.get(short_name='agent').id]
        elif ct.id in places:
            parents = [ContentTypeExtended.objects.get(short_name='place').id]
        else:
            parents = [ContentTypeExtended.objects.get(short_name='source').id]

        if ct.parents is not None:
            parents = parents + ct.parents.split(',')

        for p_id in parents:
            if p_id:
                ct.parents_list.add(ContentTypeExtended.objects.get(pk=p_id))


def collection_attribute_types(apps, schema_editor):  # noqa: ARG001
    """Create collection attribute types."""
    AttributeType = apps.get_model("dalme_app", "AttributeType")  # noqa: N806

    AttributeType.objects.create(
        name='Collection metadata',
        short_name='collection_metadata',
        description='A series of key-value pairs defining metadata values associated with a collection.',
        data_type='JSON',
        source='DALME',
    )

    AttributeType.objects.create(
        name='Workset Progress Tracking',
        short_name='workset_progress',
        description='Data attribute for tracking progress in a workset-type collection.',
        data_type='JSON',
        source='DALME',
    )


def sets_to_collections(apps, schema_editor):  # noqa: ARG001
    """Migrate sets to collections."""
    ContentType = apps.get_model('contenttypes', 'ContentType')  # noqa: N806
    Set = apps.get_model("dalme_app", "Set")  # noqa: N806
    Collection = apps.get_model("dalme_app", "Collection")  # noqa: N806
    Permission = apps.get_model("dalme_app", "Permission")  # noqa: N806
    Attribute = apps.get_model("dalme_app", "Attribute")  # noqa: N806
    AttributeType = apps.get_model("dalme_app", "AttributeType")  # noqa: N806
    CollectionMembership = apps.get_model("dalme_app", "CollectionMembership")  # noqa: N806
    Comment = apps.get_model("dalme_app", "Comment")  # noqa: N806
    Set_x_content = apps.get_model("dalme_app", "Set_x_content")  # noqa: N806
    Source = apps.get_model("dalme_app", "Source")  # noqa: N806

    for target in Set.objects.all():
        # create new collection and populate basic attributes
        use_as_ws = target.set_type == 4  # noqa: PLR2004
        new_collection = Collection.objects.create(
            id=target.id,
            name=target.name,
            description=target.description,
            use_as_workset=use_as_ws,
            published=target.is_public,
        )

        # transfer metadata
        new_collection.creation_user = target.creation_user
        new_collection.modification_user = target.modification_user
        new_collection.creation_timestamp = target.creation_timestamp
        new_collection.modification_timestamp = target.modification_timestamp
        new_collection.owner = target.owner

        if target.dataset_usergroup:
            new_collection.team_link = target.dataset_usergroup

        new_collection.save()

        # create entry in dict for matching later
        # SET_MATCH_DICT[target.id] = new_collection.id
        new_col_ct = ContentType.objects.get(app_label='dalme_app', model='collection')
        group_ct = ContentType.objects.get(app_label='auth', model='group')
        source_ct = ContentType.objects.get(app_label='dalme_app', model='source')

        # create attributes based on set type
        # stat_title & stat_text => to json-field attribute
        if target.stat_title is not None and target.stat_text is not None:
            Attribute.objects.create(
                content_type=new_col_ct,
                object_id=new_collection.id,
                attribute_type=AttributeType.objects.get(short_name='collection_metadata'),
                value_JSON={target.stat_title: target.stat_text},
            )

        # workset tracking
        members = Set_x_content.objects.filter(set_id=target.id)

        if target.set_type == 4:  # noqa: PLR2004
            workset_progress = [str(s.object_id) for s in members if s.workset_done]

            Attribute.objects.create(
                content_type=new_col_ct,
                object_id=new_collection.id,
                attribute_type=AttributeType.objects.get(short_name='workset_progress'),
                value_JSON=workset_progress,
            )

        # assign members
        for member in members:
            link = CollectionMembership(
                collection=new_collection,
                content_type=source_ct,
                object_id=Source.objects.get(pk=member.object_id).id,
                creation_user=member.creation_user,
                modification_user=member.modification_user,
                creation_timestamp=member.creation_timestamp,
                modification_timestamp=member.modification_timestamp,
            )
            link.save()

        # migrate permissions
        # 1. default permissions
        Permission.objects.create(
            content_type=new_col_ct,
            object_id=new_collection.id,
            is_default=True,
            can_view=target.permissions != 1,
            can_add=target.permissions not in [1, 2],
            can_remove=target.permissions == 4,  # noqa: PLR2004
        )

        # 2. permissions by dataset_usergroup (and user?)
        if target.dataset_usergroup is not None:
            ds_group = target.dataset_usergroup
            Permission.objects.create(
                content_type=new_col_ct,
                object_id=new_collection.id,
                principal_type=group_ct,
                principal_id=ds_group.id,
                can_view=True,
                can_add=True,
                can_remove=True,
            )

        # migrate comments / reassign foreign key
        set_ct = ContentType.objects.get(app_label='dalme_app', model='set')
        comments = Comment.objects.filter(content_type=set_ct, object_id=target.id)
        for comment in comments:
            comment.content_type = new_col_ct
            comment.object_id = new_collection.id
            comment.save()


def set_source_permissions(apps, schema_editor):  # noqa: ARG001
    """Set source permissions."""
    Permission = apps.get_model("dalme_app", "Permission")  # noqa: N806
    ContentType = apps.get_model('contenttypes', 'ContentType')  # noqa: N806
    Source = apps.get_model("dalme_app", "Source")  # noqa: N806

    group_ct = ContentType.objects.get(app_label='auth', model='group')
    source_ct = ContentType.objects.get(app_label='dalme_app', model='source')

    for source in Source.objects.all():
        if source.is_private:
            Permission.objects.create(
                content_type=source_ct,
                object_id=source.id,
                is_default=True,
                can_view=False,
            )
        elif source.primary_dataset is not None:
            ds_group = source.primary_dataset.dataset_usergroup
            Permission.objects.create(
                content_type=source_ct,
                object_id=source.id,
                principal_type=group_ct,
                principal_id=ds_group.id,
                can_view=True,
                can_edit=True,
            )


def migrate_task_data(apps, schema_editor):  # noqa: ARG001
    """Migrate task data."""
    Task = apps.get_model("dalme_app", "Task")  # noqa: N806

    for task in Task.objects.all():
        if task.completed is True:
            task.completed_by = task.modification_user
            task.save()

        if task.assigned_to is not None:
            task.assignees.add(task.assigned_to)

        if task.file is not None:
            task.files.add(task.file)

        if task.workset is not None:
            task.resources.add(task.workset)


class Migration(migrations.Migration):  # noqa: D101
    atomic = False
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0005_sql_casts'),
    ]

    operations = [
        migrations.RunPython(update_content_types),
        migrations.RunPython(collection_attribute_types),
        migrations.RunPython(sets_to_collections),
        migrations.RunPython(set_source_permissions),
        migrations.RunPython(migrate_task_data),
    ]
