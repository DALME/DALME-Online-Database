from django.conf import settings
from django.db import migrations
from django.db.utils import IntegrityError


def fix_agent_duplicates(apps, schema_editor):  # noqa: ARG001
    """Update content types."""
    Agent = apps.get_model('dalme_app', 'Agent')  # noqa: N806
    SourceCredits = apps.get_model('dalme_app', 'Source_credit')  # noqa: N806

    control = []
    concordance = {}
    for agent in Agent.objects.order_by('creation_timestamp'):
        if agent.user in control:
            concordance[agent.id] = agent.user
        else:
            control.append(agent.user)

    for old_id, user_id in concordance.items():
        concordance[old_id] = Agent.objects.filter(user=user_id).order_by('creation_timestamp').first().id

    for record in SourceCredits.objects.all():
        if record.agent.id in concordance:
            new_agent = Agent.objects.get(pk=concordance[record.agent.id])
            try:
                record.agent = new_agent
                record.save()
            except IntegrityError:
                record.delete()

    for a_id in list(concordance.keys()):
        dup = Agent.objects.get(pk=a_id)
        dup.delete()


class Migration(migrations.Migration):  # noqa: D101
    atomic = False
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(fix_agent_duplicates),
    ]
