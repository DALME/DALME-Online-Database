"""Serializers for editor data."""

from rest_framework import serializers

from domain.api.serializers import DynamicSerializer
from domain.models import Element, ElementSet, ElementSetMembership, ElementTag, ElementTagAttribute


class ElementTagAttributeSerializer(serializers.ModelSerializer):
    """Serializer for TEI element tag attributes."""

    options = serializers.SerializerMethodField()

    class Meta:
        model = ElementTagAttribute
        fields = [
            'label',
            'value',
            'kind',
            'description',
            'required',
            'editable',
            'default',
            'options',
        ]

    def get_options(self, obj):
        if obj.options:
            return obj.options.get_values(tenanted=False)
        return None


class ElementTagSerializer(DynamicSerializer):
    """Serializer for TEI element tags."""

    attributes = ElementTagAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = ElementTag
        fields = [
            'id',
            'element',
            'name',
            'kind',
            'placeholder',
            'parent',
            'icon',
            'attributes',
        ]


class ElementSerializer(serializers.ModelSerializer):
    """Serializer for TEI elements."""

    tags = ElementTagSerializer(fields=['id'], many=True, read_only=True)

    class Meta:
        model = Element
        fields = [
            'id',
            'label',
            'section',
            'description',
            'kb_reference',
            'tags',
            'compound',
            'icon',
        ]


class ElementSetMemberSerializer(serializers.ModelSerializer):
    """Serializer for TEI element set members."""

    class Meta:
        model = ElementSetMembership
        fields = [
            'element',
            'in_context_menu',
            'in_toolbar',
            'shortcut',
        ]


class ElementSetSerializer(serializers.ModelSerializer):
    """Serializer for TEI element sets."""

    members = ElementSetMemberSerializer(many=True, read_only=True)
    project = serializers.ReadOnlyField(source='project.name')

    class Meta:
        model = ElementSet
        fields = [
            'id',
            'label',
            'description',
            'project',
            'is_default',
            'members',
        ]
