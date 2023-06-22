from dalme_app.models import LanguageReference

from .base_classes import DynamicSerializer


class LanguageReferenceSerializer(DynamicSerializer):
    """Serializer for languages."""

    class Meta:  # noqa: D106
        model = LanguageReference
        fields = ('id', 'glottocode', 'iso6393', 'name', 'is_dialect', 'parent')
        field_sets = {
            'option': ['id', 'name'],
            'attribute': ['id', 'name', 'iso6393'],
        }


# LanguageReferenceSerializer._declared_fields['parent'] = LanguageReferenceSerializer(
#     field_set='attribute',
# )
