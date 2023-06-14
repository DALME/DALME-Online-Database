from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):  # noqa: D101
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dalme_app', '0004_attribute_value_models'),
    ]
    # this is a workaround for an issue filtering over generic relations in postgres
    # when UUID foreign keys are stored in text/char fields
    # this is a known and long-standing bug in Django: https://code.djangoproject.com/ticket/16055#no2
    # the problem still exists, despite being ostensibly fixed with a patch in 2023:
    # https://github.com/django/django/pull/16632/files#diff-ca59ee7c2039f916cf688bb872c67dd07447d3475b6b6b279092a53dbc0c38ab
    operations = [
        migrations.RunSQL("CREATE CAST (character varying AS uuid) WITH INOUT AS IMPLICIT;"),
        migrations.RunSQL("CREATE CAST (uuid AS character varying) WITH INOUT AS IMPLICIT;"),
    ]
