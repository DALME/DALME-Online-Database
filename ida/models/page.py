"""Pages model."""

import json

import requests

from django.apps import apps
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.db.models import options

from ida.models import AttributeType
from ida.models.resourcespace import rs_api_query
from ida.models.templates import IDAUuid

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class Page(IDAUuid):
    """Stores page information."""

    name = models.CharField(max_length=55)
    dam_id = models.IntegerField(db_index=True, null=True)
    order = models.IntegerField(db_index=True)
    canvas = models.TextField(blank=True, null=True)
    tags = GenericRelation('ida.Tag')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    @property
    def manifest_url(self):
        """Return IIIF manifest for the page."""
        return f'{settings.DAM_URL}/loris/{self.dam_id}/info.json'

    @property
    def thumbnail_url(self):
        """Return the thumbnail's url for the image associated with the page (if any)."""
        rs_resource = apps.get_model(app_label='ida', model_name='rs_resource')
        try:
            thumbnail = rs_resource.objects.get(ref=self.dam_id).get_image_url('thm')
        except (KeyError, ValueError):
            thumbnail = None

        return thumbnail

    @property
    def transcription(self):
        """Return transcription page associated with the page (if any)."""
        folio_model = apps.get_model(app_label='ida', model_name='pagenode')
        folio = folio_model.objects.filter(page=self)
        return folio.first().transcription if folio.exists() else None

    @property
    def has_image(self):
        """Return boolean indicating if there is an image associated with the page."""
        return bool(self.dam_id)

    @property
    def has_transcription(self):
        """Return boolean indicating if there is a transcription associated with the page."""
        return bool(self.transcription)

    def get_rights(self):
        """Return the rights information for the image associated with the page (if any)."""
        try:
            record = self.records.first().record
            rights_atype = AttributeType.objects.get(name='default_rights')
            parent_rights = record.parent.attributes.filter(attribute_type=rights_atype.id)

            if not parent_rights.exists():
                parent_rights = record.parent.parent.attributes.filter(attribute_type=rights_atype.id)

            if parent_rights.exists():
                rights = parent_rights.first()
                return {
                    'show_image': rights.value.public_display,
                    'status': rights.value.get_rights_status_display(),
                    'display_notice': rights.value.notice_display,
                    'notice': rights.value.rights_notice,
                }
            else:  # noqa: RET505
                return None

        except AttributeError:
            return None

    def get_absolute_url(self):
        """Return the absolute url for the instance."""
        record = self.records.first().record
        return f'{record.get_absolute_url()}{self.name}/'

    def get_canvas(self):
        """Return IIIF canvas associated with the page."""
        if self.dam_id is not None:
            api_params = {
                'function': 'get_resource_data',
                'param1': self.dam_id,
            }
            page_meta = rs_api_query(**api_params)
            page_meta_obj = page_meta.json()

            if isinstance(page_meta_obj, list):
                folio = page_meta_obj[0]['field79']
            elif isinstance(page_meta_obj, dict):
                folio = page_meta_obj['field79']
            canvas = requests.get(f'{settings.DAM_URL}/iiif/{self.dam_id}/canvas/{folio}')
            canvas_dict = json.loads(canvas.text)
            canvas_dict['page_id'] = str(self.id)
            self.canvas = json.dumps(canvas_dict)

        return self.canvas
