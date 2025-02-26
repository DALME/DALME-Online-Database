"""Options-related models."""

from django.apps import apps
from django.db import models
from django.db.models import options

from app.abstract import TrackingMixin
from tenants.models import TenantMixin

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

    def get_values(self, serialize=True, raw_data=False, public=False, tenanted=True, model=None, filters=None):  # noqa: PLR0913
        values = self.values.all() if tenanted else self.values.unscoped()
        if not values.exists():
            return None

        if public and values.filter(public=True).exists():
            payload = values.filter(public=True).first().payload
        else:
            payload = values.first().payload

        concordance = None
        model_name = None

        if self.payload_type == 'db_records':
            model_name = model if model and payload.get('model') == 'TBD' else payload.get('model')
            target_model = apps.get_model(payload.get('app'), model_name)
            target_filters = {**payload.get('filters'), **filters} if filters else payload.get('filters')
            concordance = payload.get('concordance')
            order = payload.get('order')

            if hasattr(target_model, 'attribute_list'):
                data = (
                    target_model.unattributed.filter(**target_filters)
                    if target_filters
                    else target_model.unattributed.all()
                )
            else:
                data = target_model.objects.filter(**target_filters) if target_filters else target_model.objects.all()

            if order:
                data = data.order_by(*order)

        elif self.payload_type == 'field_choices':
            model_name = model if model else payload.get('model')
            target_model = apps.get_model(payload.get('app'), model_name)
            choices = getattr(target_model, payload.get('choices'))
            data = [{'label': i[1], 'value': i[0]} for i in choices]

        elif self.payload_type == 'static_list':
            data = payload

        if raw_data:
            return data

        if serialize:
            serializer = OptionsSerializer(data, many=True, concordance=concordance, model_name=model_name)
            return serializer.data

        value_name = concordance.get('value', 'value') if concordance else 'value'
        label_name = concordance.get('label', 'label') if concordance else 'label'
        return (
            [(i.get(value_name), i.get(label_name)) for i in data]
            if isinstance(data[0], dict)
            else [(getattr(i, value_name), getattr(i, label_name)) for i in data]
        )


class OptionsValue(TenantMixin, TrackingMixin):
    """Stores tenanted static lists of values."""

    op_list = models.ForeignKey(OptionsList, on_delete=models.CASCADE, related_name='values')
    payload = models.JSONField()
    public = models.BooleanField(default=False)
