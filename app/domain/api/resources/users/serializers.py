"""Serializers for user data."""

from drf_writable_nested.serializers import WritableNestedModelSerializer
from rest_framework import serializers

from django.contrib.auth import get_user_model

from app.abstract import BASE_DATA_TYPES
from domain.api.serializers import DynamicSerializer
from domain.models.preference import Preference


class PreferenceSerializer(serializers.ModelSerializer):
    """Serializes user preference data."""

    data_type = serializers.ChoiceField(BASE_DATA_TYPES, source='key.data_type')
    description = serializers.CharField(source='key.description')
    group = serializers.CharField(max_length=55, source='key.group')
    label = serializers.CharField(max_length=255, source='key.label')
    name = serializers.CharField(max_length=55, source='key.name')

    class Meta:
        model = Preference
        fields = [
            'data_type',
            'description',
            'group',
            'label',
            'name',
            'value',
        ]


class UserSerializer(DynamicSerializer, WritableNestedModelSerializer):
    """Serializes user and profile data."""

    avatar = serializers.URLField(max_length=255, source='avatar_url', required=False)
    group_ids = serializers.PrimaryKeyRelatedField(source='groups', required=False, read_only=True, many=True)
    preferences = PreferenceSerializer(many=True, required=False)
    # option fields
    detail = serializers.ReadOnlyField(source='username')
    icon = serializers.URLField(max_length=255, source='avatar_url', required=False)
    label = serializers.ReadOnlyField(source='full_name')
    value = serializers.IntegerField(source='id')

    class Meta:
        model = get_user_model()
        fields = [
            'avatar',
            'date_joined',
            'detail',
            'email',
            'first_name',
            'full_name',
            'group_ids',
            'icon',
            'id',
            'is_active',
            'is_staff',
            'is_superuser',
            'label',
            'last_login',
            'last_name',
            'password',
            'preferences',
            'username',
            'value',
        ]
        default_exclude = [
            'detail',
            'icon',
            'label',
            'value',
        ]
        restricted = [
            'date_joined',
            'email',
            'group_ids',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'preferences',
            'password',
        ]
        field_sets = {
            'attribute': [
                'avatar',
                'email',
                'full_name',
                'id',
                'username',
            ],
            'option': [
                'detail',
                'icon',
                'label',
                'value',
            ],
        }
        extra_kwargs = {
            'password': {
                'required': False,
                'write_only': True,
            },
            'username': {
                'validators': [],
            },
        }
