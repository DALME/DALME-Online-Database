from django.contrib.messages import constants
from django.core.management import call_command

from dalme_app.models import Page, rs_resource


def update_rs_folio_field(user_id):
    """Update folio field in RS database."""
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
    message = f'{message}, but the following pages had errors: {", ".join(errors)}' if errors else f'{message}.'

    return {'message': message, 'level': constants.WARNING, 'user_id': user_id}


def update_search_index():
    """Update the search index."""
    call_command('search_index', '--rebuild', '-f')


def wagtail_publish_pages():
    """Publish schaduled Wagtail pages."""
    call_command('publish_scheduled_pages')


def test_task(user_id):
    """Task for testing."""
    return {'message': 'Test task completed.', 'level': constants.INFO, 'user_id': user_id}
