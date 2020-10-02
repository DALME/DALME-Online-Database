
from django.contrib.auth.models import User
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

        if data.get('user', {}).get('id') is not None:
            data['user']['username'] = User.objects.get(pk=data['user']['id']).username

        return super().to_internal_value(data)

    def run_validation(self, data):
        validated_data = super().run_validation(data)

        if validated_data.get('user') is not None:
            validated_data['user'] = User.objects.get(username=validated_data['user']['username'])

        return validated_data
