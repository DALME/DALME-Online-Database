"""Serializers for tenant data."""
from rest_framework import serializers

from ida.models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    """Serializer for tenants."""

    class Meta:
        model = Tenant
        fields = [
            'id',
            'name',
        ]
