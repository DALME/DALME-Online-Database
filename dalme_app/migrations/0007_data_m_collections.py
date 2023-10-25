from django.conf import settings
from django.db import migrations


def collection_attribute_types(apps, schema_editor):
    """Create collection attribute types."""
    AttributeType = apps.get_model('dalme_app', 'AttributeType')  # noqa: N806
    User = apps.get_model('auth', 'User')  # noqa: N806

    user_obj = User.objects.get(pk=1)

    print('\n\nCreating new attribute types `collection_metadata` and `workset_progress`...', end='')  # noqa: T201

    AttributeType.objects.create(
        name='Collection metadata',
        short_name='collection_metadata',
        description='A series of key-value pairs defining metadata values associated with a collection.',
        data_type='JSON',
        source='DALME',
        creation_user=user_obj,
        modification_user=user_obj,
    )

    AttributeType.objects.create(
        name='Workset Progress Tracking',
        short_name='workset_progress',
        description='Data attribute for tracking progress in a workset-type collection.',
        data_type='JSON',
        source='DALME',
        creation_user=user_obj,
        modification_user=user_obj,
    )

    print(' \033[94m\033[1mOK\033[0m')  # noqa: T201


def sets_to_collections(apps, schema_editor):
    """Migrate sets to collections."""
    ContentType = apps.get_model('contenttypes', 'ContentType')  # noqa: N806
    Set = apps.get_model('dalme_app', 'Set')  # noqa: N806
    Collection = apps.get_model('dalme_app', 'Collection')  # noqa: N806
    Permission = apps.get_model('dalme_app', 'Permission')  # noqa: N806
    Attribute = apps.get_model('dalme_app', 'Attribute')  # noqa: N806
    AttributeType = apps.get_model('dalme_app', 'AttributeType')  # noqa: N806
    CollectionMembership = apps.get_model('dalme_app', 'CollectionMembership')  # noqa: N806
    Comment = apps.get_model('dalme_app', 'Comment')  # noqa: N806
    Set_x_content = apps.get_model('dalme_app', 'Set_x_content')  # noqa: N806
    Record = apps.get_model('dalme_app', 'Record')  # noqa: N806
    User = apps.get_model('auth', 'User')  # noqa: N806

    user_obj = User.objects.get(pk=1)
    new_col_ct = ContentType.objects.get(app_label='dalme_app', model='collection')
    group_ct = ContentType.objects.get(app_label='auth', model='group')
    record_ct = ContentType.objects.get(app_label='dalme_app', model='record')

    sets = Set.objects.all()
    count = 0

    print(f'Migrating {len(sets)} sets...', end='')  # noqa: T201

    for target in sets:
        # create new collection and populate basic attributes + transfer metadata
        use_as_ws = target.set_type == 4  # noqa: PLR2004
        new_collection = Collection.objects.create(
            id=target.id,
            name=target.name,
            use_as_workset=use_as_ws,
            is_published=target.is_public,
            creation_user=target.creation_user,
            modification_user=target.modification_user,
            creation_timestamp=target.creation_timestamp,
            modification_timestamp=target.modification_timestamp,
            owner=target.owner,
        )

        if target.dataset_usergroup:
            new_collection.team_link = target.dataset_usergroup

        new_collection.save(update_fields=['team_link'])

        if target.description:
            Attribute.objects.create(
                content_type=new_col_ct,
                object_id=new_collection.id,
                attribute_type=AttributeType.objects.get(short_name='description'),
                value_TXT=target.description,
                creation_user=user_obj,
                modification_user=user_obj,
            )

        # create attributes based on set type
        # stat_title & stat_text => to json-field attribute
        if target.stat_title is not None and target.stat_text is not None:
            Attribute.objects.create(
                content_type=new_col_ct,
                object_id=new_collection.id,
                attribute_type=AttributeType.objects.get(short_name='collection_metadata'),
                value_JSON={target.stat_title: target.stat_text},
                creation_user=user_obj,
                modification_user=user_obj,
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
                creation_user=user_obj,
                modification_user=user_obj,
            )

        # assign members
        for member in members:
            CollectionMembership.objects.create(
                collection=new_collection,
                content_type=record_ct,
                object_id=Record.objects.get(pk=member.object_id).id,
                creation_user=member.creation_user,
                modification_user=member.modification_user,
                creation_timestamp=member.creation_timestamp,
                modification_timestamp=member.modification_timestamp,
            )

        # migrate permissions
        # 1. default permissions
        Permission.objects.create(
            content_type=new_col_ct,
            object_id=new_collection.id,
            is_default=True,
            can_view=target.permissions != 1,
            can_add=target.permissions not in [1, 2],
            can_remove=target.permissions == 4,  # noqa: PLR2004
            creation_user=user_obj,
            modification_user=user_obj,
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
                creation_user=user_obj,
                modification_user=user_obj,
            )

        # migrate comments / reassign foreign key
        set_ct = ContentType.objects.get(app_label='dalme_app', model='set')
        comments = Comment.objects.filter(content_type=set_ct, object_id=target.id)
        for comment in comments:
            comment.content_type = new_col_ct
            comment.object_id = new_collection.id
            comment.save(update_fields=['content_type', 'object_id'])

        count += 1

    print(' \033[94m\033[1mOK\033[0m')  # noqa: T201
    print(f'{count} collections created.')  # noqa: T201
    print('  Overall migration...', end='')  # noqa: T201


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0006_update_content_types'),
    ]

    operations = [
        migrations.RunPython(collection_attribute_types),
        migrations.RunPython(sets_to_collections),
    ]
