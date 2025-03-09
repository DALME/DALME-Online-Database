"""API endpoint for managing languages."""

import re
from itertools import groupby

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework.decorators import action
from rest_framework.response import Response

from app.access_policies import BaseAccessPolicy
from domain.api.viewsets import BaseViewSet
from domain.models import Attribute, AttributeType, LanguageReference

from .serializers import LanguageReferenceSerializer


class LanguageAccessPolicy(BaseAccessPolicy):
    """Access policies for the Languages endpoint."""

    id = 'languages-policy'


class Languages(BaseViewSet):
    """API endpoint for managing languages."""

    permission_classes = [LanguageAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & LanguageAccessPolicy]

    queryset = LanguageReference.objects.all()
    serializer_class = LanguageReferenceSerializer
    filterset_fields = ['id', 'name', 'is_dialect', 'parent__name', 'iso6393', 'glottocode']
    search_fields = ['id', 'name', 'is_dialect', 'parent__name', 'iso6393', 'glottocode']
    ordering_fields = ['id', 'name', 'is_dialect', 'parent', 'iso6393', 'glottocode']
    ordering = ['name']

    @action(detail=True, methods=['post'])
    def completions(self, request, *args, **kwargs):  # noqa: ARG002
        """Get completions for language."""
        try:
            word = request.data['word']
            language = self.get_object()
            lang_attr = AttributeType.objects.get(name='language')
            records = [
                a.content_object
                for a in Attribute.objects.filter(attribute_type=lang_attr.id, value__id=f'{language.id}')
            ]

            blobs = []
            for record in records:
                for page in record.pages.all():
                    if page.transcription:
                        blobs.append(page.transcription.text_blob)

            blob = ' '.join(blobs)
            tokens = re.findall(r'\w+', blob)
            tokens.sort()
            counts = [(x, len(list(y))) for x, y in groupby(tokens)]
            counts.sort(key=lambda x: x[1], reverse=True)
            # completions = [
            #     {
            #         'label': 'match',
            #         'type': 'keyword',
            #         # 'info': '(World)',
            #         # 'apply': '⠁⭒*.✩.*⭒⠁',
            #         # 'detail': 'macro',
            #     }
            # ]

            completions = [{'label': i, 'type': 'token'} for i in [t[0] for t in counts] if i.startswith(word)]

            return Response(completions, 200)

        except Exception as e:  # noqa: BLE001
            return Response({'error': str(e)}, 400)
