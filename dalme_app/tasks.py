from __future__ import absolute_import, unicode_literals
from dalme_app.models import (Page, rs_resource)
from celery import shared_task
from django.core.management import call_command


@shared_task
def update_rs_folio_field():
    pages = Page.objects.exclude(dam_id__isnull=True)
    for page in pages:
        rs_image = rs_resource.objects.get(ref=page.dam_id)
        rs_image.field79 = page.name
        rs_image.save()


@shared_task
def update_search_index():
    call_command('search_index', '--rebuild', '-f')


@shared_task
def wagtail_publish_pages():
    call_command('publish_scheduled_pages')
