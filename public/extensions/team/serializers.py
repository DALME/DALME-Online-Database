"""Serializers for team extension."""

from rest_framework import serializers

from .models import TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    """Team member serializer."""

    class Meta:
        model = TeamMember
        fields = ['name']
