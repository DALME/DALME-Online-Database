"""Serializers for ticket data."""
from django_currentuser.middleware import get_current_user
from rest_framework import serializers
from rest_framework.utils import model_meta

from django.contrib.auth import get_user_model
from django.utils import timezone

from dalme_api.resources.attachments import AttachmentSerializer
from dalme_api.resources.comments import CommentSerializer
from dalme_api.resources.tags import TagSerializer
from dalme_api.resources.users import UserSerializer
from dalme_app.models import Attachment, Tag, Ticket


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for tickets."""

    tags = TagSerializer(many=True, required=False)
    file = AttachmentSerializer(required=False)
    creation_user = UserSerializer(field_set='attribute', required=False)
    modification_user = UserSerializer(field_set='attribute', required=False)
    closing_user = UserSerializer(field_set='attribute', required=False)
    assigned_to = UserSerializer(field_set='attribute', required=False)

    class Meta:
        model = Ticket
        fields = (
            'id',
            'assigned_to',
            'subject',
            'description',
            'status',
            'tags',
            'url',
            'file',
            'closing_user',
            'closing_date',
            'comment_count',
            'creation_user',
            'creation_timestamp',
            'modification_user',
            'modification_timestamp',
        )
        extra_kwargs = {
            'tags': {'required': False},
        }

    def to_internal_value(self, data):
        """Transform incoming data."""
        if data.get('tags') is not None:
            self.context['tags'] = data.pop('tags')
        return super().to_internal_value(data)

    def create(self, validated_data):
        """Create new ticket."""
        tags = self.context.get('tags')
        ticket = Ticket.objects.create(**validated_data)
        if tags:
            for tag in tags:
                obj = {'tag_type': 'T', 'tag': tag}
                ticket.tags.create(**obj)
        return ticket


class TicketDetailSerializer(serializers.ModelSerializer):
    """Serializer for single instance tickets."""

    tags = TagSerializer(many=True, required=False)
    file = AttachmentSerializer(required=False)
    creation_user = UserSerializer(fields=['full_name', 'username', 'id', 'avatar'], required=False)
    modification_user = UserSerializer(fields=['full_name', 'username', 'id', 'avatar'], required=False)
    comments = CommentSerializer(many=True, required=False)
    assigned_to = UserSerializer(fields=['full_name', 'username', 'id', 'avatar'], required=False)
    closing_user = UserSerializer(fields=['full_name', 'username', 'id', 'avatar'], required=False)

    class Meta:
        model = Ticket
        fields = (
            'id',
            'subject',
            'description',
            'status',
            'tags',
            'url',
            'file',
            'comments',
            'comment_count',
            'closing_user',
            'closing_date',
            'creation_user',
            'creation_timestamp',
            'modification_user',
            'modification_timestamp',
            'assigned_to',
        )
        extra_kwargs = {
            'tags': {'required': False},
        }

    def to_internal_value(self, data):
        """Transform incoming data."""
        if data.get('tags') is not None:
            self.context['tags'] = data.pop('tags')
        if data.get('assigned_to') is not None:
            self.context['assigned_to'] = data.pop('assigned_to')
        if data.get('file') is not None:
            self.context['file'] = data.pop('file')
        return super().to_internal_value(data)

    def update(self, instance, validated_data):  # noqa: C901,PLR0912
        """Update ticket data."""
        serializers.raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        assigned_to = self.context.get('assigned_to')
        tags = self.context.get('tags')
        file = self.context.get('file')
        fields = ['modification_user', 'modification_timestamp']
        m2m_fields = []
        validated_data['modification_user'] = get_current_user()

        if validated_data.get('status') is not None and validated_data['status'] == 1:
            validated_data.update(
                {
                    'closing_user': get_current_user(),
                    'closing_date': timezone.now(),
                },
            )

        if assigned_to:
            validated_data['assigned_to'] = get_user_model().objects.get(id=assigned_to)

        if file:
            validated_data['file'] = Attachment.objects.get(id=file)

        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                fields.append(attr)
                setattr(instance, attr, value)

        instance.save(update_fields=fields)

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        if tags:
            if instance.tags.all().exists():
                new_tags = []
                current_tags = {i.tag: i.id for i in instance.tags.all()}
                for tag in tags:
                    if current_tags.get(tag) is None:
                        new_tags.append(tag)
                    else:
                        current_tags.pop(tag)

                if len(current_tags) > 0:
                    for tag in current_tags.values():
                        Tag.objects.get(id=tag).delete()
            else:
                new_tags = tags

            if new_tags:
                for tag in new_tags:
                    instance.tags.create(tag=tag)

        return super().update(instance, validated_data)

    @staticmethod
    def process_tags(instance, tags):
        if instance.tags.all().exists():
            new_tags = []
            current_tags = {i.tag: i.id for i in instance.tags.all()}
            for tag in tags:
                if current_tags.get(tag) is None:
                    new_tags.append(tag)
                else:
                    current_tags.pop(tag)

            if len(current_tags) > 0:
                for tag in current_tags.values():
                    Tag.objects.get(id=tag).delete()
        else:
            new_tags = tags

        if new_tags:
            for tag in new_tags:
                instance.tags.create(tag=tag)
