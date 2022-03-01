from rest_framework import status
from rest_framework.response import Response

from django.contrib.auth.models import User

from dalme_api import api
from dalme_api.v2_serializers import AttributeOptionsSerializer
from dalme_app.models import (
    Attribute,
    Attribute_type,
    CountryReference,
    LanguageReference,
    LocaleReference,
    RightsPolicy,
    Set,
    Source,
)


class Attributes(api.Attributes):
    """Endpoint for the Attribute resource."""

    def get_serializer_class(self):
        if self.request.GET.get('options'):
            return AttributeOptionsSerializer
        return super().get_serializer_class()

    def get_queryset(self, *args, **kwargs):
        if self.request.GET.get('options'):
            short_name = self.request.GET['options']
            return self.get_options(short_name)
        return super().get_queryset(*args, **kwargs)

    def get_options(self, short_name):
        try:
            attribute_type = Attribute_type.objects.get(short_name=short_name)
        except Attribute_type.DoesNotExist:
            Response(status=status.HTTP_404_NOT_FOUND)
        return self.resolve_data(short_name, attribute_type)

    def resolve_data(self, short_name, attribute_type):
        return {
            'created_by': self.get_user_options(),
            'last_user': self.get_user_options(),
            'owner': self.get_user_options(),
            'parent': [
                {'label': obj.short_name, 'value': obj.id}
                for obj in Source.objects.all().order_by('name')
            ],
            'authority': [
                {'label': 'Church', 'value': 'Church'},
                {'label': 'Court', 'value': 'Court'},
                {'label': 'Notary', 'value': 'Notary'},
            ],
            'country': [
                {'label': obj.name, 'value': obj.name}
                for obj in CountryReference.objects.all().order_by('name')
            ],
            'default_rights': [
                {'label': obj.name, 'value': obj.id}
                for obj in RightsPolicy.objects.all().order_by('name')
            ],
            'format': [
                {'label': 'Charter', 'value': 'Charter'},
                {'label': 'Register - demi-quarto', 'value': 'Register - demi-quarto'},
                {'label': 'Register - quarto', 'value': 'Register - quarto'},
            ],
            'language': [
                {'label': obj['name'], 'value': obj['id'], 'caption': obj['iso6393']}
                for obj in LanguageReference.objects.filter(
                    iso6393__isnull=False
                ).order_by('name').values('id', 'name', 'iso6393')
            ],
            'language_gc': [
                {'label': obj['name'], 'value': obj['id'], 'caption': obj['glottocode']}
                for obj in LanguageReference.objects.filter(
                    glottocode__isnull=False
                ).order_by('name').values('id', 'name', 'glottocode')
            ],
            'locale': [
                {'label': obj.name, 'value': obj.id}
                for obj in LocaleReference.objects.all().order_by('name')
            ],
            'permissions': [
                {'label': label, 'value': value}
                for value, label in Set._meta.get_field('permissions').choices
            ],
            'record_type': [
                {'label': obj['value_STR'], 'value': obj['value_STR']}
                for obj in Attribute.objects.filter(
                    attribute_type=attribute_type, value_STR__isnull=False
                ).values('value_STR').distinct()
            ],
            'rights_status': [
                {'label': 'Copyrighted', 'value': 'Copyrighted'},
                {'label': 'Orphaned', 'value': 'Orphaned'},
                {'label': 'Owned', 'value': 'Owned'},
                {'label': 'Public Domain', 'value': 'Public Domain'},
            ],
            'same_as': None,  # TODO: List all AttributeType, should exclude asame_as in that case
            'set_type': [
                {'label': label, 'value': value}
                for value, label in Set._meta.get_field('set_type').choices
            ],
            'support': [
                {'label': 'Paper', 'value': 'Paper'},
                {'label': 'Parchment', 'value': 'Parchment'},
                {'label': 'Vellum', 'value': 'Vellum'},
            ],
        }[short_name]

    @staticmethod
    def get_user_options():
        return [
            {'label': obj.profile.full_name, 'value': obj.id, 'caption': obj.email}
            # TODO: Only need the isnull check as jhrr doesn't have a profile.
            for obj in User.objects.filter(profile__isnull=False)
        ]
