"""Options-related models."""

from django.apps import apps
from django.db import models
from django.db.models import options

from app.abstract import TrackingMixin
from tenants.models.tenant import TenantMixin

from .options_serializer import OptionsSerializer

options.DEFAULT_NAMES = (*options.DEFAULT_NAMES, 'in_db')


class OptionsList(TrackingMixin):
    """Stores lists of attribute value options. Payload format as follows.

    `db_records`: {
        'app': FOO,
        'model': BAR,
        'filters': {'is_active': True}, # queryset filters as dict, optional
        'concordance': {'label': FOO.BAR, 'value': BAZ, 'group': BAY, # optional 'detail': BAX, # optional},
    }
    `field_choices`: {
        'app': FOO,
        'model': BAR,
        'choices': BAZ
    }
    `static_list`: [
        {'label': FOO, 'value': BAR, 'group': BAZ, # optional 'detail': BAY, # optional},
        ...
    ]
    """

    PAYLOAD_TYPES = (
        ('db_records', 'DB Records'),
        ('field_choices', 'Field Choices'),
        ('static_list', 'Static List'),
    )

    name = models.CharField(max_length=255)
    payload_type = models.CharField(max_length=15, choices=PAYLOAD_TYPES)
    description = models.TextField()

    def get_values(self, serialize=True, public=False):
        if not self.values.exists():
            return None

        if public and self.values.filter(public=True).exists():
            payload = self.values.filter(public=True).first().payload
        else:
            payload = self.values.first().payload

        concordance = None
        if self.payload_type == 'db_records':
            model = apps.get_model(payload.get('app'), payload.get('model'))
            filters = payload.get('filters')
            data = model.objects.filter(**filters) if filters else model.objects.all()
            concordance = payload.get('concordance')

        elif self.payload_type == 'field_choices':
            model = apps.get_model(payload.get('app'), payload.get('model'))
            choices = getattr(model, payload.get('choices'))
            data = [{'label': i[1], 'value': i[0]} for i in choices]

        elif self.payload_type == 'static_list':
            data = payload

        if serialize:
            serializer = OptionsSerializer(data, many=True, concordance=concordance)
            return serializer.data

        value_name = concordance.get('value', 'value') if concordance else 'value'
        label_name = concordance.get('label', 'label') if concordance else 'label'
        return [(getattr(i, value_name), getattr(i, label_name)) for i in data]


class OptionsValue(TenantMixin, TrackingMixin):
    """Stores tenanted static lists of values."""

    op_list = models.ForeignKey(OptionsList, on_delete=models.CASCADE, related_name='values')
    payload = models.JSONField()
    public = models.BooleanField(default=False)
