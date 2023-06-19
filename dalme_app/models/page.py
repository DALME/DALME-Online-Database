import json

import requests

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from dalme_app.models.resourcespace import rs_api_query, rs_resource
from dalme_app.models.templates import dalmeUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Page(dalmeUuid):
    """Stores page information."""

    name = models.CharField(max_length=55)
    dam_id = models.IntegerField(db_index=True, null=True)
    order = models.IntegerField(db_index=True)
    canvas = models.TextField(blank=True)
    tags = GenericRelation('Tag')

    class Meta:  # noqa: D106
        ordering = ['order']

    def __str__(self):  # noqa: D105
        return self.name

    @property
    def manifest_url(self):
        """Return IIIF manifest for the page."""
        return f'https://dam.dalme.org/loris/{self.dam_id}/info.json'

    @property
    def thumbnail_url(self):
        """Return the thumbnail's url for the image associated with the page (if any)."""
        try:
            thumbnail = rs_resource.objects.get(ref=self.dam_id).get_image_url('thm')
        except (KeyError, ValueError):
            thumbnail = None

        return thumbnail

    def get_rights(self):
        """Return the rights information for the image associated with the page (if any)."""
        try:
            source = self.sources.first().source
            parent_rights = source.parent.attributes.filter(attribute_type=144)

            if not parent_rights.exists():
                parent_rights = source.parent.parent.attributes.filter(attribute_type=144)

            if parent_rights.exists():
                return {
                    'show_image': parent_rights.value.public_display,
                    'status': parent_rights.value.get_rights_status_display(),
                    'display_notice': parent_rights.value.notice_display,
                    'notice': parent_rights.value.rights_notice,
                }
            else:  # noqa: RET505
                return None

        except AttributeError:
            return None

    def get_absolute_url(self):
        """Return the absolute url for the instance."""
        source = self.sources.first().source
        return f'{source.get_absolute_url()}{self.name}/'

    def get_canvas(self):
        """Return IIIF canvas associated with the page."""
        # need to find way to prevent stored canvas from getting stale
        # or to determine if it is...
        if self.dam_id is not None:
            api_params = {
                'function': 'get_resource_data',
                'param1': self.dam_id,
            }
            page_meta = rs_api_query(**api_params)
            page_meta_obj = page_meta.json()

            if type(page_meta_obj) is list:
                folio = page_meta_obj[0]['field79']
            elif type(page_meta_obj) is dict:
                folio = page_meta_obj['field79']

            canvas = requests.get(f'https://dam.dalme.org/iiif/{self.dam_id}/canvas/{folio}')
            canvas_dict = json.loads(canvas.text)
            canvas_dict['page_id'] = str(self.id)
            self.canvas = json.dumps(canvas_dict)

        return self.canvas
