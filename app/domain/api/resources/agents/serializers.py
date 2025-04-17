"""Serializers for agent data."""

from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from domain.api.resources.users import UserSerializer
from domain.api.serializers import DynamicSerializer
from domain.models import Agent


class AgentSerializer(DynamicSerializer, WritableNestedModelSerializer):
    """Serializer for Agents."""

    user = UserSerializer(required=False)
    agent_type = serializers.CharField(source='get_agent_type_display')
    record_attestation_count = serializers.SerializerMethodField()

    class Meta:
        model = Agent
        fields = [
            'id',
            'agent_type',
            'name',
            'user',
            'attestation_count',
            'record_attestation_count',
        ]
        extra_kwargs = {
            'notes': {
                'required': False,
            },
            'user': {
                'required': False,
            },
        }

    def get_record_attestation_count(self, obj):
        """Return count of attestations for current record."""
        if self.context.get('record'):
            return obj.get_attestations_for_record(self.context['record'])
        return None

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
