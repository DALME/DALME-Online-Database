from django.db import migrations


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('ida', '0001_initial'),
    ]
    operations = [
        # the following SQL statements are a workaround for an issue filtering over generic relations in postgres
        # when UUID foreign keys are stored in text/char fields
        # this is a known and long-standing bug in Django: https://code.djangoproject.com/ticket/16055#no2
        # the problem still exists, despite being ostensibly fixed with a patch in 2023:
        # https://github.com/django/django/pull/16632/files#diff-ca59ee7c2039f916cf688bb872c67dd07447d3475b6b6b279092a53dbc0c38ab
        migrations.RunSQL('CREATE CAST (character varying AS uuid) WITH INOUT AS IMPLICIT;'),
        migrations.RunSQL('CREATE CAST (uuid AS character varying) WITH INOUT AS IMPLICIT;'),
        migrations.RunSQL('CREATE CAST (character varying AS integer) WITH INOUT AS IMPLICIT;'),
        migrations.RunSQL('CREATE CAST (integer AS character varying) WITH INOUT AS IMPLICIT;'),
    ]
