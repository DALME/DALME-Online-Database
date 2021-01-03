from dalme_app.models import Page, rs_resource
from django.core.management import call_command
from django.contrib.messages import constants


def update_rs_folio_field(user_id):
    pages = Page.objects.exclude(dam_id__isnull=True)
    errors = []
    for page in pages:
        try:
            dam_id = int(page.dam_id)
        except ValueError:
            errors.append(page.id)
            continue
        if rs_resource.objects.filter(ref=dam_id).exists():
            rs_image = rs_resource.objects.get(ref=page.dam_id)
            rs_image.field79 = page.name
            rs_image.save()

    message = 'Folio names were updated in the DAM'
    if errors:
        message += f", but the following pages had errors: {', '.join(errors)}"
    else:
        message += '.'

    result = {
        'message': message,
        'level': constants.WARNING,
        'user_id': user_id
    }

    return result


def update_search_index(user_id):
    call_command('search_index', '--rebuild', '-f')


def wagtail_publish_pages():
    call_command('publish_scheduled_pages')


def test_task(user_id):
    return {
        'message': 'Test task completed.',
        'level': constants.INFO,
        'user_id': user_id
    }
