
from dalme_app.models import Agent
from ._common import DynamicSerializer
from dalme_app.serializers.users import UserSerializer


class AgentSerializer(DynamicSerializer):
    user = UserSerializer(fields=['full_name', 'username', 'id'], required=False)

    class Meta:
        model = Agent
        fields = ('id', 'type', 'standard_name', 'notes', 'user')
        extra_kwargs = {
            'notes': {'required': False},
            'user': {'required': False},
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['type'] = {
            'id': instance.type,
            'name': instance.get_type_display()
        }
        return ret

    def to_internal_value(self, data):
        if data.get('type', {}).get('id') is not None:
            data['type'] = data['type']['id']

        return super().to_internal_value(data)
