"""Serializers for agent data."""

from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from domain.api.serializers import DynamicSerializer
from domain.models import Agent


class AgentSerializer(DynamicSerializer, WritableNestedModelSerializer):
    """Serializer for Agents."""

    agent_type = serializers.CharField(source='get_agent_type_display')
    record_attestation_count = serializers.SerializerMethodField()
    user_id = serializers.PrimaryKeyRelatedField(source='user', required=False, read_only=True)

    class Meta:
        model = Agent
        fields = [
            'agent_type',
            'attestation_count',
            'id',
            'name',
            'record_attestation_count',
            'user_id',
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
