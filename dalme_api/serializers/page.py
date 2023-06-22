from dalme_app.models import Page

from .base_classes import DynamicSerializer


class PageSerializer(DynamicSerializer):
    """Serializer for pages."""

    class Meta:  # noqa: D106
        model = Page
        fields = ('id', 'name', 'order', 'dam_id', 'thumbnail_url', 'manifest_url')
        field_sets = {
            'option': ['id', 'name', 'order', 'thumbnail_url'],
            'attribute': ['id', 'name', 'dam_id'],
        }
        extra_kwargs = {
            'dam_id': {'required': False},
            'thumbnail_url': {'required': False},
            'manifest_url': {'required': False},
        }

    def run_validation(self, data):
        """Run validation on serializer data."""
        _id = data['id'] if data.get('id') is not None else False
        data = {k: v for k, v in data.items() if v is not None}
        validated_data = super().run_validation(data)
        if _id:
            validated_data['id'] = _id
        return validated_data
