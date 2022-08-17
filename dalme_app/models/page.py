from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
import requests
import json
from dalme_app.models._templates import dalmeUuid
import django.db.models.options as options
from dalme_app.models.rights_policy import RightsPolicy
from dalme_app.models.resourcespace import rs_api_query

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
            parent_rights = source.parent.attributes.filter(attribute_type=144)

            if not parent_rights.exists():
                parent_rights = source.parent.parent.attributes.filter(attribute_type=144)

            if parent_rights.exists():
                rpo = RightsPolicy.objects.get(pk=parent_rights.first().value_JSON['id'])
                return {
                    'show_image': rpo.public_display,
                    'status': rpo.get_rights_status_display(),
                    'display_notice': rpo.notice_display,
                    'notice': rpo.rights_notice
                    }
            else:
                return None

        except AttributeError:
            return None

    def get_absolute_url(self):
        source = self.sources.first().source
        return f'{source.get_absolute_url()}{self.name}/'

    def get_canvas(self):
        # need to find way to prevent stored canvas from getting stale
        # or to determine if it is...
        if self.dam_id is not None:
            api_params = {
                "function": "get_resource_data",
                "param1": self.dam_id
            }
            page_meta = rs_api_query(**api_params)
            page_meta_obj = page_meta.json()
            if type(page_meta_obj) is list:
                folio = page_meta_obj[0]['field79']
            elif type(page_meta_obj) is dict:
                folio = page_meta_obj['field79']
            canvas = requests.get("https://dam.dalme.org/iiif/{}/canvas/{}".format(self.dam_id, folio))
            canvas_dict = json.loads(canvas.text)
            canvas_dict['page_id'] = str(self.id)
            self.canvas = json.dumps(canvas_dict)
            return self.canvas
        else:
            return self.canvas
