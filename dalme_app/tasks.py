from __future__ import absolute_import, unicode_literals
from dalme_app.models import (Page, rs_resource)
from celery import shared_task
from async_messages import messages
from django.contrib.auth.models import User
from django.core.management import call_command


@shared_task
def update_rs_folio_field(user_id):
    user = User.objects.get(id=user_id)
    try:
        pages = Page.objects.all()
        for page in pages:
            rs_image = rs_resource.objects.get(ref=page.dam_id)
            rs_image.field79 = page.name
            rs_image.save()
        messages.success(user, 'The folio ids on the DAM have been updated.')
    except Exception as e:
        messages.error(user, 'The folio ids on the DAM could not be updated because of the following error: ' + str(e))


@shared_task
def update_search_index():
    call_command('update_index', '--remove')


@shared_task
def wagtail_publish_pages():
    call_command('publish_scheduled_pages')
