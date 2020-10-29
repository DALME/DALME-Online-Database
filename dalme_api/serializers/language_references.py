from dalme_app.models import LanguageReference
from rest_framework import serializers


class LanguageReferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LanguageReference
        fields = ('id', 'glottocode', 'iso6393', 'name', 'type', 'parent')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        if ret.get('parent') is not None:
            ret['parent'] = {
                'name': instance.parent.name,
                'id': instance.parent.id
                }
        if ret.get('type') is not None:
            ret['type'] = {
                'name': instance.get_type_display(),
                'id': instance.type
                }
        return ret
