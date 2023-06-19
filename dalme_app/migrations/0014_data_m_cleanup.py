from django.conf import settings
from django.db import migrations


def update_content_type_ontology(apps, schema_editor):  # noqa: ARG001, C901
    """Bring ContentAttributeTypes table up to date."""
    Attribute = apps.get_model('dalme_app', 'Attribute')  # noqa: N806
    AttributeType = apps.get_model('dalme_app', 'AttributeType')  # noqa: N806
    apps.get_model('contenttypes', 'ContentType')
    ContentAttributeTypes = apps.get_model('dalme_app', 'ContentAttributeTypes')  # noqa: N806
    ContentTypeExtended = apps.get_model("dalme_app", "ContentTypeExtended")  # noqa: N806
    User = apps.get_model("auth", "User")  # noqa: N806

    user_obj = User.objects.get(pk=1)

    print('\n')  # noqa: T201
    for target in ContentTypeExtended.objects.filter(content_type__isnull=False):
        print(f'Processing cte type {target.short_name}:')  # noqa: T201
        att_used = []
        for att in Attribute.objects.filter(content_type__id=target.id):
            if att.attribute_type.id not in att_used:
                att_used.append(att.attribute_type.id)

        print(f'Initial used count = {len(att_used)}.')  # noqa: T201

        att_present = []
        for att in ContentAttributeTypes.objects.filter(content_type__id=target.id):
            if att.attribute_type.id not in att_present:
                att_present.append(att.attribute_type.id)

        print(f'Present count = {len(att_present)}.')  # noqa: T201

        att_to_remove = [i for i in att_present if i not in att_used]
        att_to_add = [i for i in att_used if i not in att_present]

        if len(att_to_remove) > 0:
            print(  # noqa: T201
                f'Present but not used: {", ".join([AttributeType.objects.get(pk=i).short_name for i in att_to_remove])}.',
            )
            for atype_id in att_to_remove:
                atype = AttributeType.objects.get(pk=atype_id)
                if not atype.is_local and atype.data_type != 'RREL':
                    instance = ContentAttributeTypes.objects.get(
                        content_type__id=target.id,
                        attribute_type__id=atype_id,
                    )
                    instance.delete()

        if len(att_to_add) > 0:
            print(  # noqa: T201
                f'Used but not present: {", ".join([AttributeType.objects.get(pk=i).short_name for i in att_to_add])}.',
            )
            for atype_id in att_to_add:
                atype = AttributeType.objects.get(pk=atype_id)
                ContentAttributeTypes.objects.create(
                    content_type=target,
                    attribute_type=atype,
                    creation_user=user_obj,
                    modification_user=user_obj,
                )


def clean_up_attribute_types(apps, schema_editor):  # noqa: ARG001
    """Remove unused attribute types."""
    ContentAttributeTypes = apps.get_model("dalme_app", "ContentAttributeTypes")  # noqa: N806
    AttributeType = apps.get_model("dalme_app", "AttributeType")  # noqa: N806
    Attribute = apps.get_model("dalme_app", "Attribute")  # noqa: N806

    used_types_ct = list({entry.attribute_type.id for entry in ContentAttributeTypes.objects.all()})
    used_types_att = list({att.attribute_type.id for att in Attribute.objects.all()})

    if len(used_types_ct) != len(used_types_att):
        if len(used_types_ct) > len(used_types_att):
            diff = [i for i in used_types_ct if i not in used_types_att]
        else:
            diff = [i for i in used_types_att if i not in used_types_ct]
    else:
        diff = []

    print(f'\n  {len(used_types_ct)} attribute types are currently in use per CT count.')  # noqa: T201
    print(f'  {len(used_types_att)} attribute types are currently in use per ATT count.')  # noqa: T201

    if len(diff) > 0:
        print(  # noqa: T201
            f'  The extra types are: {", ".join([AttributeType.objects.get(pk=i).short_name for i in diff])}.',
        )

    used_types = list(set(used_types_ct + used_types_att))
    count = 0
    removed = []

    for atype in AttributeType.objects.all():
        if atype.id not in used_types and not atype.is_local and atype.data_type != 'RREL':
            removed.append(atype.short_name)
            atype.delete()
            count += 1

    print(f'  {count} attribute types removed from DB.')  # noqa: T201
    print(', '.join(removed))  # noqa: T201


class Migration(migrations.Migration):  # noqa: D101
    atomic = False
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0013_remove_unused'),
    ]

    operations = [
        migrations.RunPython(update_content_type_ontology),
        migrations.RunPython(clean_up_attribute_types),
    ]
