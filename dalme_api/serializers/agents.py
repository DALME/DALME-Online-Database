"""Interface for dalme_api.serializers.agents module."""
from drf_writable_nested.serializers import WritableNestedModelSerializer

from dalme_api.serializers.users import UserSerializer
from dalme_app.models import Agent

from .base_classes import DynamicSerializer


class AgentSerializer(DynamicSerializer, WritableNestedModelSerializer):
    """Serializer for Agents."""

    user = UserSerializer(required=False)

    class Meta:
        model = Agent
        fields = ('id', 'agent_type', 'name', 'user')
        extra_kwargs = {
            'notes': {'required': False},
            'user': {'required': False},
        }

    # def to_internal_value(self, data):
    #     """Transform incoming data."""
    #     if data.get('type', {}).get('id') is not None:
    #         data['type'] = data['type']['id']

    #     if data.get('user', {}).get('id') is not None:
    #         data['user']['username'] = User.objects.get(pk=data['user']['id']).username

    #     return super().to_internal_value(data)

    # def run_validation(self, data):
    #     """Run validation on serializer data."""
    #     validated_data = super().run_validation(data)

    #     if validated_data.get('user') is not None:
    #         validated_data['user'] = User.objects.get(username=validated_data['user']['username'])

    #     return validated_data
