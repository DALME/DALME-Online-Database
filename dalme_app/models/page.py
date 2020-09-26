from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
import json
import requests
from dalme_app.models._templates import dalmeUuid
import django.db.models.options as options
import dalme_app.models.rights_policy as _rights_policy
import dalme_app.models.resourcespace as _resourcespace

options.DEFAULT_NAMES = options.DEFAULT_NAMES + ('in_db',)


class Page(dalmeUuid):
    name = models.CharField(max_length=55)
    dam_id = models.IntegerField(db_index=True, null=True)
    order = models.IntegerField(db_index=True)
    canvas = models.TextField(null=True)
    tags = GenericRelation('Tag')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

    def get_rights(self):
        try:
            source = self.sources.first().source
            exists = source.parent.parent.attributes.filter(
                attribute_type=144
            ).exists()
        except AttributeError:
            return None

        if exists:
            rpo = _rights_policy.RightsPolicy.objects.get(
                pk=json.loads(
                    source.parent.parent.attributes.get(attribute_type=144).value_STR
                )['id'])
            return {
                'status': rpo.get_rights_status_display(),
                'display_notice': rpo.notice_display,
                'notice': json.loads(rpo.rights_notice)
            }
        return None

    def get_absolute_url(self):
        return reverse('page_detail', kwargs={'pk': self.pk})

    def get_canvas(self):
        if not self.canvas and self.dam_id is not None:
            api_params = {
                "function": "get_resource_data",
                "param1": self.dam_id
            }
            page_meta = _resourcespace.rs_api_query(**api_params)
            page_meta_obj = page_meta.json()
            if type(page_meta_obj) is list:
                folio = page_meta_obj[0]['field79']
            elif type(page_meta_obj) is dict:
                folio = page_meta_obj['field79']
            canvas = requests.get("https://dam.dalme.org/iiif/{}/canvas/{}".format(self.dam_id, folio))
            self.canvas = canvas.text
            return canvas.text
        else:
            return self.canvas
