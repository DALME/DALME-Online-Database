
from dalme_app.models import Agent
from ._common import DynamicSerializer
import dalme_app.serializers.users as _users


class AgentSerializer(DynamicSerializer):
    user = _users.UserSerializer(fields=['full_name', 'username', 'id'])

    class Meta:
        model = Agent
        fields = ('id', 'type', 'standard_name', 'notes', 'user')

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['type'] = {
            'id': instance.type,
            'name': instance.get_type_display()
        }
        return ret
