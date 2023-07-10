from rest_framework import serializers

from django.db import models

from dalme_api.serializers.users import GroupSerializer, UserSerializer
from dalme_app.models import Collection, CollectionMembership

from .attributes import AttributeSerializer
from .base_classes import DynamicSerializer
from .records import RecordSerializer  # noqa: F401


class CollectionMemberList(serializers.ListSerializer):
    """Ensures item-appropriate serializer is used for each instance in list."""

    def __init__(self, *args, **kwargs):  # noqa: D107
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
            serializer_class = eval(f'{item._meta.model.__name__}Serializer')  # noqa: PGH001, SLF001
            ret.append(serializer_class(item, field_set='collection_member').data)

        return ret


class CollectionMemberSerializer(serializers.ModelSerializer):
    """Serializer for mixed content type collection members."""

    class Meta:  # noqa: D106
        model = CollectionMembership
        fields = ('content_object',)
        list_serializer_class = CollectionMemberList


class CollectionSerializer(DynamicSerializer):
    """Serializer for collections."""

    id = serializers.ReadOnlyField()  # noqa: A003
    attributes = AttributeSerializer(many=True, required=False)
    owner = UserSerializer(field_set='attribute', required=False)
    team_link = GroupSerializer(field_set='attribute', required=False)
    # members = CollectionMemberSerializer(many=True)
    creation_user = UserSerializer(field_set='attribute', required=False)
    modification_user = UserSerializer(field_set='attribute', required=False)
    is_private = serializers.BooleanField()

    class Meta:  # noqa: D106
        model = Collection
        fields = (
            'id',
            'name',
            'attributes',
            'use_as_workset',
            'is_published',
            'is_private',
            'owner',
            'team_link',
            'creation_timestamp',
            'modification_timestamp',
            'creation_user',
            'modification_user',
            # 'members',
            'member_count',
            'comment_count',
        )
        field_sets = {
            'option': ['id', 'name', 'is_published', 'is_private'],
            'attribute': [
                'id',
                'name',
                'is_published',
                'is_private',
                'use_as_workset',
                'owner',
                'team_link',
                'member_count',
            ],
        }
