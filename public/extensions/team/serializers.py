"""Serializers for team extension."""

from rest_framework import serializers

from django.contrib import auth

from .models import TeamMember


class TeamMemberSerializer(serializers.ModelSerializer):
    """Team member serializer."""

    username = serializers.CharField(max_length=255, source='user.username', required=False)
    avatar = serializers.CharField(max_length=255, source='avatar_url', required=False)

    class Meta:
        model = TeamMember
        fields = ['id', 'name', 'username', 'avatar']


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    name = serializers.CharField(max_length=255, source='wagtail_userprofile.profile.full_name', required=False)
    avatar = serializers.CharField(max_length=255, source='wagtail_userprofile.profile.profile_image', required=False)

    class Meta:
        model = auth.get_user_model()
        fields = ['id', 'name', 'username', 'avatar']
