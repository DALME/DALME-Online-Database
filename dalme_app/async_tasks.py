from __future__ import absolute_import, unicode_literals
""" Celery tasks """
from dalme_app.models import (Page, rs_resource)
from dalme.celeryapp import app
from async_messages import messages
from django.contrib.auth.models import User


# to invoke task, use: task_name.apply_async()
@app.task
def update_rs_folio_field(user_id):
    try:
        pages = Page.objects.all()
        for page in pages:
            rs_image = rs_resource.objects.get(ref=page.dam_id)
            rs_image.field79 = page.name
            rs_image.save()
        user = User.objects.get(id=user_id)
        messages.success(user, 'The folio ids on the DAM have been updated.')
    except Exception as e:
        messages.error(user, 'The folio ids on the DAM could not be updated because of the following error: ' + str(e))
