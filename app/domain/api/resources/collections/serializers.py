"""Serializers for collection data."""

from rest_framework import serializers

from django.db import models

from domain.api.resources.attributes import AttributeSerializer
from domain.api.resources.groups import GroupSerializer
from domain.api.resources.tenants import TenantSerializer
from domain.api.resources.users import UserSerializer
from domain.api.serializers import DynamicSerializer
from domain.models import Collection, CollectionMembership


class CollectionMemberList(serializers.ListSerializer):
    """Ensures item-appropriate serializer is used for each instance in list."""

    def __init__(self, *args, **kwargs):
        self.child = kwargs.pop('child', None)
        self.allow_empty = kwargs.pop('allow_empty', True)
        self.max_length = kwargs.pop('max_length', None)
        self.min_length = kwargs.pop('min_length', None)

        instance = kwargs.get('instance', [])
        data = kwargs.get('data', [])
        if instance and data:
            assert len(data) == len(instance), 'Data and instance should have same length'

        super(serializers.ListSerializer, self).__init__(*args, **kwargs)

    def to_representation(self, data):
        """Override method to use serializer class instead of instance."""
        iterable = data.all() if isinstance(data, models.manager.BaseManager) else data
        iterable = [i.content_object for i in iterable]
        ret = []

        for item in iterable:
            serializer_class = eval(f'{item._meta.model.__name__}Serializer')  # noqa: SLF001
            ret.append(serializer_class(item, field_set='collection_member').data)

        return ret


class CollectionMemberSerializer(serializers.ModelSerializer):
    """Serializer for mixed content type collection members."""

    tenant = TenantSerializer(required=True)

    class Meta:
        model = CollectionMembership
        list_serializer_class = CollectionMemberList
        fields = [
            'tenant',
            'content_object',
        ]


class CollectionSerializer(DynamicSerializer):
    """Serializer for collections."""

    # members = CollectionMemberSerializer(many=True)
    attributes = AttributeSerializer(many=True, required=False)
    attribute_ids = serializers.PrimaryKeyRelatedField(source='attributes', required=False, read_only=True, many=True)
    creation_user = UserSerializer(field_set='attribute', required=False)
    creation_user_id = serializers.PrimaryKeyRelatedField(source='creation_user', required=False, read_only=True)
    id = serializers.ReadOnlyField()
    is_private = serializers.BooleanField()
    modification_user = UserSerializer(field_set='attribute', required=False)
    modification_user_id = serializers.PrimaryKeyRelatedField(
        source='modification_user', required=False, read_only=True
    )
    owner = UserSerializer(field_set='attribute', required=False)
    owner_id = serializers.PrimaryKeyRelatedField(source='owner', required=False, read_only=True)
    team_link = GroupSerializer(field_set='attribute', required=False)
    team_link_id = serializers.PrimaryKeyRelatedField(source='team_link', required=False, read_only=True)
    tenant = TenantSerializer(required=True)

    class Meta:
        model = Collection
        fields = [
            'attributes',
            'attribute_ids',
            'comment_count',
            'creation_timestamp',
            'creation_user',
            'creation_user_id',
            'id',
            'is_corpus',
            'is_private',
            'is_published',
            'member_count',
            'modification_timestamp',
            'modification_user',
            'modification_user_id',
            'name',
            'owner',
            'owner_id',
            'team_link',
            'team_link_id',
            'tenant',
            'use_as_workset',
            # 'members',
        ]
        field_sets = {
            'option': [
                'id',
                'is_private',
                'is_published',
                'name',
            ],
            'attribute': [
                'id',
                'is_private',
                'is_published',
                'member_count',
                'name',
                'owner',
                'team_link',
                'use_as_workset',
            ],
            'retrieve': [
                'attribute_ids',
                'comment_count',
                'creation_timestamp',
                'creation_user_id',
                'id',
                'is_corpus',
                'is_private',
                'is_published',
                'member_count',
                'modification_timestamp',
                'modification_user_id',
                'name',
                'owner_id',
                'team_link_id',
                'tenant',
                'use_as_workset',
            ],
        }
