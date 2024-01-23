# Generated by Django 4.2.2 on 2024-01-17 14:28

from django.db import migrations


def ensure_profile(apps, schema_editor):
    """Make sure all users have a a profile record."""
    User = apps.get_model('ida', 'User')  # noqa: N806
    Profile = apps.get_model('ida', 'Profile')  # noqa: N806

    objs = User.objects.filter(profile__isnull=True)
    for obj in objs:
        Profile.objects.create(user=obj, full_name=f'{obj.first_name} {obj.last_name}')
        print(f'Created profile record for user: {obj}')  # noqa: T201


class Migration(migrations.Migration):
    dependencies = [
        ('ida', '0036_auto_20240117_0837'),
    ]

    operations = [
        migrations.RunPython(ensure_profile),
    ]