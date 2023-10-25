from django.conf import settings
from django.db import migrations
from django.db.utils import IntegrityError


def fix_agent_duplicates(apps, schema_editor):
    """Update content types."""
    Agent = apps.get_model('dalme_app', 'Agent')  # noqa: N806
    SourceCredits = apps.get_model('dalme_app', 'Source_credit')  # noqa: N806

    control = []
    concordance = {}

    print('\n\n\t\033[36mFixing agent duplicates:\033[0m')  # noqa: T201

    print('Generating concordance list...', end='')  # noqa: T201
    for agent in Agent.objects.order_by('creation_timestamp'):
        if agent.user in control:
            concordance[agent.id] = agent.user
        else:
            control.append(agent.user)

    for old_id, user_id in concordance.items():
        concordance[old_id] = Agent.objects.filter(user=user_id).order_by('creation_timestamp').first().id
    print(' \033[94m\033[1mOK\033[0m')  # noqa: T201

    print('\033[95mFixing references in SourceCredits...\033[0m', end='')  # noqa: T201
    for record in SourceCredits.objects.all():
        if record.agent.id in concordance:
            new_agent = Agent.objects.get(pk=concordance[record.agent.id])
            try:
                record.agent = new_agent
                record.save()
            except IntegrityError:
                record.delete()
    print(' \033[94m\033[1mOK\033[0m')  # noqa: T201

    print('Deleting duplicates...', end='')  # noqa: T201
    for a_id in list(concordance.keys()):
        dup = Agent.objects.get(pk=a_id)
        dup.delete()
    print(' \033[94m\033[1mOK\033[0m')  # noqa: T201

    print('  Overall migration...', end='')  # noqa: T201


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL('ALTER TYPE varchar OWNER TO dalme;'),
        migrations.RunPython(fix_agent_duplicates),
        # the following SQL statements are a workaround for an issue filtering over generic relations in postgres
        # when UUID foreign keys are stored in text/char fields
        # this is a known and long-standing bug in Django: https://code.djangoproject.com/ticket/16055#no2
        # the problem still exists, despite being ostensibly fixed with a patch in 2023:
        # https://github.com/django/django/pull/16632/files#diff-ca59ee7c2039f916cf688bb872c67dd07447d3475b6b6b279092a53dbc0c38ab
        migrations.RunSQL('CREATE CAST (character varying AS uuid) WITH INOUT AS IMPLICIT;'),
        migrations.RunSQL('CREATE CAST (uuid AS character varying) WITH INOUT AS IMPLICIT;'),
        migrations.RunSQL('CREATE CAST (character varying AS integer) WITH INOUT AS IMPLICIT;'),
        migrations.RunSQL('CREATE CAST (integer AS character varying) WITH INOUT AS IMPLICIT;'),
        # the next commands are necessary because when migrating from MySQL to Postgres
        # certain constraints were created as indices and Postgres doesn't look for indices
        # when altering constraints, so we drop the index and recreate it as a constraint proper
        migrations.RunSQL('DROP INDEX idx_16430_dalme_app_attribute_object_id_attribute_type_c83849ec;'),
        migrations.RunSQL(
            'ALTER TABLE public.dalme_app_attribute ADD CONSTRAINT idx_16430_dalme_app_attribute_object_id_attribute_type_c83849ec UNIQUE(object_id, attribute_type, "value_STR");',
        ),
        migrations.RunSQL('DROP INDEX idx_16554_dalme_app_set_x_content_content_type_id_object_i_8838;'),
        migrations.RunSQL(
            'ALTER TABLE public.dalme_app_set_x_content ADD CONSTRAINT idx_16554_dalme_app_set_x_content_content_type_id_object_i_8838 UNIQUE(content_type_id, object_id, set_id_id);',
        ),
        migrations.RunSQL('DROP INDEX idx_16558_dalme_app_source_type_name_37ac523f_uniq;'),
        migrations.RunSQL(
            'ALTER TABLE public.dalme_app_source ADD CONSTRAINT idx_16558_dalme_app_source_type_name_37ac523f_uniq UNIQUE(type, name);',
        ),
        migrations.RunSQL('DROP INDEX idx_16561_dalme_app_source_credit_source_id_agent_id_type_2bd09;'),
        migrations.RunSQL(
            'ALTER TABLE public.dalme_app_source_credit ADD CONSTRAINT idx_16561_dalme_app_source_credit_source_id_agent_id_type_2bd09 UNIQUE(source_id, agent_id, type);',
        ),
        migrations.RunSQL('DROP INDEX idx_16580_dalme_app_tasklist_group_id_slug_82602101_uniq;'),
        migrations.RunSQL(
            'ALTER TABLE public.dalme_app_tasklist ADD CONSTRAINT idx_16580_dalme_app_tasklist_group_id_slug_82602101_uniq UNIQUE(group_id, slug);',
        ),
    ]
