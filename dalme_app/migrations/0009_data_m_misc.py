from django.conf import settings
from django.db import migrations


def migrate_task_data(apps, schema_editor):  # noqa: ARG001
    """Migrate task data."""
    Task = apps.get_model("dalme_app", "Task")  # noqa: N806

    for task in Task.objects.all():
        if task.completed is True:
            task.completed_by = task.modification_user
            task.save(update_fields=['completed_by'])

        if task.assigned_to is not None:
            task.assignees.add(task.assigned_to)

        if task.file is not None:
            task.files.add(task.file)

        if task.workset is not None:
            task.resources.add(task.workset)


def create_credit_support_records(apps, schema_editor):  # noqa: ARG001
    """Create records necessary to migrate source credits."""
    ScopeType = apps.get_model("dalme_app", "ScopeType")  # noqa: N806
    RelationshipType = apps.get_model("dalme_app", "RelationshipType")  # noqa: N806
    Scope = apps.get_model("dalme_app", "Scope")  # noqa: N806
    User = apps.get_model("auth", "User")  # noqa: N806

    user_obj = User.objects.get(pk=1)

    # authorship (type), credit (scope), editor (qualifier)
    RelationshipType.objects.create(
        name='Authorship',
        short_name='authorship',
        is_directed=True,
        description='The source is, in some capacity, responsible for the creation of the target.',
        creation_user=user_obj,
        modification_user=user_obj,
    )

    ScopeType.objects.create(
        name='Temporal',
        short_name='temporal',
        description='Target is time-constrained within a range (expressed as "start" and "end" parameters) or a duration (as "duration").',
        creation_user=user_obj,
        modification_user=user_obj,
    )

    ScopeType.objects.create(
        name='Spatial',
        short_name='spatial',
        description='Target is spatially-constrained to a geographic location expressed as one of: "polygon" (GIS geometry), "point" (coordinates), or "location" (named, e.g. country, locale, etc.). Point and location can be augmented with an "extents" parameter indicating a ditance from them.',
        creation_user=user_obj,
        modification_user=user_obj,
    )

    ScopeType.objects.create(
        name='Linguistic',
        short_name='linguistic',
        description='Target applies only in the context of a linguistic system, such as a language, dialect, or writing system. Expressed as a reference to a Language Reference record.',
        creation_user=user_obj,
        modification_user=user_obj,
    )

    ctx_scope = ScopeType(
        name='Contextual',
        short_name='contextual',
        description='Target is limited to a specific context, broadly defined. A catch-all category designed to help refine the ontology in future.',
        creation_user=user_obj,
        modification_user=user_obj,
    )
    ctx_scope.save()

    Scope.objects.create(
        scope_type=ctx_scope,
        parameters={'credit': 'editor'},
        notes='Qualifies an authorship relationship, limiting its effects to the receipt of credit in the category indicated by the "credit" parameter. E.g. editor, contributor, corrections.',
        creation_user=user_obj,
        modification_user=user_obj,
    )

    Scope.objects.create(
        scope_type=ctx_scope,
        parameters={'credit': 'contributor'},
        notes='Qualifies an authorship relationship, limiting its effects to the receipt of credit in the category indicated by the "credit" parameter. E.g. editor, contributor, corrections.',
        creation_user=user_obj,
        modification_user=user_obj,
    )

    Scope.objects.create(
        scope_type=ctx_scope,
        parameters={'credit': 'corrections'},
        notes='Qualifies an authorship relationship, limiting its effects to the receipt of credit in the category indicated by the "credit" parameter. E.g. editor, contributor, corrections.',
        creation_user=user_obj,
        modification_user=user_obj,
    )


def migrate_source_credits(apps, schema_editor):  # noqa: ARG001
    """Migrate records from source credits to relationships."""
    SourceCredits = apps.get_model("dalme_app", "SourceCredits")  # noqa: N806
    Scope = apps.get_model("dalme_app", "Scope")  # noqa: N806
    RelationshipType = apps.get_model("dalme_app", "RelationshipType")  # noqa: N806
    Relationship = apps.get_model("dalme_app", "Relationship")  # noqa: N806
    ContentType = apps.get_model('contenttypes', 'ContentType')  # noqa: N806

    scope_ed = Scope.objects.get(parameters__credit='editor')
    scope_corr = Scope.objects.get(parameters__credit='corrections')
    scope_cont = Scope.objects.get(parameters__credit='contributor')
    authorship = RelationshipType.objects.get(short_name='authorship')
    ct_agent = ContentType.objects.get(app_label='dalme_app', model='agent')
    ct_source = ContentType.objects.get(app_label='dalme_app', model='source')

    for record in SourceCredits.objects.all():
        new_rel = Relationship(
            source_content_type=ct_agent,
            source_object_id=record.agent.id,
            target_content_type=ct_source,
            target_object_id=record.source.id,
            rel_type=authorship,
            notes=record.note,
            creation_user=record.creation_user,
            modification_user=record.modification_user,
            creation_timestamp=record.creation_timestamp,
            modification_timestamp=record.modification_timestamp,
        )
        new_rel.save()

        if record.type == 1:
            new_rel.scopes.add(scope_ed)

        elif record.type == 2:  # noqa: PLR2004
            new_rel.scopes.add(scope_corr)

        elif record.type == 3:  # noqa: PLR2004
            new_rel.scopes.add(scope_cont)


class Migration(migrations.Migration):  # noqa: D101
    atomic = False
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0008_data_m_collections'),
    ]

    operations = [
        migrations.RunPython(migrate_task_data),
        migrations.RunPython(create_credit_support_records),
        migrations.RunPython(migrate_source_credits),
    ]
