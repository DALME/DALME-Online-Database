"""Serializers for user data."""

from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from django.contrib.auth import get_user_model

from api.dynamic_serializer import DynamicSerializer
from api.resources.groups import GroupSerializer
from app.abstract import BASE_DATA_TYPES
from domain.models.preference import Preference


class PreferenceSerializer(serializers.ModelSerializer):
    """Serializes user preference data."""

    name = serializers.CharField(max_length=55, source='key.name')
    label = serializers.CharField(max_length=255, source='key.label')
    description = serializers.CharField(source='key.description')
    data_type = serializers.ChoiceField(BASE_DATA_TYPES, source='key.data_type')
    group = serializers.CharField(max_length=55, source='key.group')

    class Meta:
        model = Preference
        fields = [
            'name',
            'label',
            'description',
            'data_type',
            'group',
            'value',
        ]


class UserSerializer(DynamicSerializer, WritableNestedModelSerializer):
    """Serializes user and profile data."""

    groups = GroupSerializer(many=True, field_set='attribute', required=False)
    avatar = serializers.URLField(max_length=255, source='avatar_url', required=False)
    preferences = PreferenceSerializer(many=True, required=False)

    class Meta:
        model = get_user_model()
        fields = [
            'id',
            'last_login',
            'is_superuser',
            'username',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'is_staff',
            'is_active',
            'date_joined',
            'groups',
            'password',
            'avatar',
            'preferences',
        ]
        field_sets = {
            'attribute': [
                'id',
                'username',
                'full_name',
                'avatar',
                'email',
            ],
            'option': [
                'id',
                'username',
                'full_name',
            ],
        }
        extra_kwargs = {
            'username': {
                'validators': [],
            },
            'password': {
                'write_only': True,
                'required': False,
            },
        }

    # def to_internal_value(self, data):
    #     """Transform incoming data."""
    #     if type(data) is int:
    #         user = get_user_model().objects.get(pk=data)
    #         data = {'id': user.id, 'username': user.username}

    #     if data.get('groups') is not None:
    #         self.context['groups'] = data.pop('groups')

    #     if data.get('profile') is not None:
    #         self.context['profile'] = data.pop('profile')

    #     return super().to_internal_value(data)

    # def update(self, instance, validated_data):
    #     """Update user record."""
    #     if self.context.get('profile') is not None:
    #         profile_data = self.context.get('profile')
    #         profile = Profile.objects.get_or_create(user=instance)

    #         if type(profile) is tuple:
    #             profile = profile[0]

    #         for attr, value in profile_data.items():
    #             setattr(profile, attr, value)

    #         profile.save()

    #     if self.context.get('groups') is not None:
    #         group_data = [i['id'] for i in self.context['groups']]
    #         instance.groups.set(group_data)

    #     return super().update(instance, validated_data)

    # def create(self, validated_data):
    #     """Create new user."""
    #     profile_data = self.context.get('profile')
    #     if 'username' in validated_data:
    #         validated_data['username'] = validated_data['username'].lower()

    #     user = get_user_model().objects.create_user(**validated_data)

    #     Profile.objects.create(user=user, **profile_data)

    #     if self.context.get('groups') is not None:
    #         group_data = [i['id'] for i in self.context['groups']]
    #         user.groups.set(group_data)

    #     Agent.objects.create(standard_name=user.profile.full_name, type=1, user=user)

    #     return user
