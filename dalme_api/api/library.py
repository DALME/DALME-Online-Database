import json
from rest_framework import viewsets
from rest_framework.response import Response
from dalme_api.access_policies import LibraryAccessPolicy
from pyzotero import zotero
from django.conf import settings


class Library(viewsets.ViewSet):
    """ API endpoint for accessing DALME Zotero Library """
    permission_classes = (LibraryAccessPolicy,)

    def list(self, request, *args, **kwargs):
        data = request.GET.get('data')
        collection = request.GET.get('collection')
        search = request.GET.get('search')
        content = request.GET.get('content')
        limit = request.GET.get('limit')

        queryset_generator = zotero.Zotero(
            settings.ZOTERO_LIBRARY_ID,
            'group',
            settings.ZOTERO_API_KEY
        )

        if data:
            record_total = queryset_generator.count_items()
            dt_request = json.loads(data)
            page = self.paginate_queryset(
                queryset_generator,
                dt_request.get('start'),
                dt_request.get('length')
            )

            result = {
                'draw': int(dt_request.get('draw')),  # cast return "draw" value as INT to prevent Cross Site Scripting (XSS) attacks
                'recordsTotal': record_total,
                'recordsFiltered': page.count_items(),
                'data': [i['data'] for i in page]
                }
        else:
            paras = {}
            if limit:
                paras['limit'] = int(limit)
            if content:
                paras['content'] = content
            if search:
                paras['q'] = search

            if collection:
                if search:
                    queryset = queryset_generator.collection_items_top(collection, **paras)
                else:
                    queryset = queryset_generator.everything(
                        queryset_generator.collection_items_top(collection, **paras)
                    )
            else:
                if not limit:
                    queryset = queryset_generator.everything(queryset_generator.top(**paras))
                else:
                    queryset = queryset_generator.top(**paras)

            result = queryset if content else [i['data'] for i in queryset]

        return Response(result)

    def paginate_queryset(self, queryset, start, length):
        if start is not None and length is not None:
            page = queryset.top(
                limit=length,
                start=start
            )
            if page is not None:
                queryset = page
            else:
                queryset = queryset.everything(
                    queryset.top()
                )

        return queryset

    def get_renderer_context(self):
        context = {
            'view': self,
            'args': getattr(self, 'args', ()),
            'kwargs': getattr(self, 'kwargs', {}),
            'request': getattr(self, 'request', None),
            'model': 'Library'
            }

        return context

    def retrieve(self, request, pk=None):
        content = request.GET.get('content')

        paras = {}
        if content:
            paras['content'] = content

        queryset_generator = zotero.Zotero(
            settings.ZOTERO_LIBRARY_ID,
            'group',
            settings.ZOTERO_API_KEY
        )

        result = queryset_generator.item(pk, **paras)

        return Response(result)
