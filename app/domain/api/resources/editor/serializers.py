"""Serializers for editor data."""

from rest_framework import serializers

from domain.models import Element, ElementAttribute, ElementSet, ElementSetMembership


class ElementAttributeSerializer(serializers.ModelSerializer):
    """Serializer for TEI element attributes."""

    options = serializers.SerializerMethodField()

    class Meta:
        model = ElementAttribute
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


class ElementSerializer(serializers.ModelSerializer):
    """Serializer for TEI elements."""

    attributes = ElementAttributeSerializer(many=True, read_only=True)

    class Meta:
        model = Element
        fields = [
            'id',
            'label',
            'kind',
            'section',
            'description',
            'kb_reference',
            'tag',
            'compound',
            'placeholder',
            'icon',
            'attributes',
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

    class Meta:
        model = ElementSet
        fields = [
            'label',
            'description',
            'is_default',
            'members',
        ]
