from dalme_app.models import CountryReference

from .base_classes import DynamicSerializer


class CountryReferenceSerializer(DynamicSerializer):
    """Serializer for countries."""

    class Meta:  # noqa: D106
        model = CountryReference
        fields = ('id', 'name', 'alpha_2_code', 'alpha_3_code', 'num_code')
        field_sets = {
            'option': ['id', 'name'],
            'attribute': ['id', 'name'],
        }
