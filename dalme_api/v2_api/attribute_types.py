from rest_framework.decorators import action
from stringcase import snakecase

from django.db.models import Q

from dalme_api import api
from dalme_app.models import Attribute, Attribute_type, Content_attributes


class AttributeTypes(api.AttributeTypes):
    """Endpoint for the AttributeType resource."""

    def get_queryset(self, *args, **kwargs):
        q_short_names = self.request.GET.get('short_names')
        if q_short_names:
            q_short_names = [
                snakecase(short_name) for short_name in q_short_names.split(',')
            ]
            return Attribute_type.objects.filter(short_name__in=q_short_names)

        return super().get_queryset(*args, **kwargs)
