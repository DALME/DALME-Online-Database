"""API endpoint for accessing Zotero libraries."""

from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from pyzotero import zotero
from rest_framework import viewsets
from rest_framework.response import Response

from api.access_policies import BaseAccessPolicy
from app.context import get_current_tenant


class LibraryAccessPolicy(BaseAccessPolicy):
    """Access policies for Library endpoint."""

    id = 'library-policy'


class Library(viewsets.ViewSet):
    """API endpoint for accessing Zotero libraries."""

    permission_classes = [LibraryAccessPolicy]
    oauth_permission_classes = [TokenHasReadWriteScope & LibraryAccessPolicy]

    def list(self, request, *args, **kwargs):  # noqa: ARG002
        """Return list of bibliographic sources."""
        collection = request.GET.get('collection')
        search = request.GET.get('search')
        content = request.GET.get('content')
        limit = request.GET.get('limit')
        tenant = get_current_tenant()
        queryset_generator = zotero.Zotero(
            tenant.project.zotero_library_id,
            'group',
            tenant.project.zotero_api_key,
        )

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
                    queryset_generator.collection_items_top(collection, **paras),
                )

        elif not limit:
            queryset = queryset_generator.everything(queryset_generator.top(**paras))
        else:
            queryset = queryset_generator.top(**paras)

        result = queryset if content else [i['data'] for i in queryset]

        return Response(result)

    # def paginate_queryset(self, queryset, start, length):
    #     if start is None and length is None:
    #         return queryset
    #     page = queryset.top(limit=length, start=start)
    #     return page if page is not None else queryset.everything(queryset.top())

    # def get_renderer_context(self):
    #     context = {
    #         'view': self,
    #         'args': getattr(self, 'args', ()),
    #         'kwargs': getattr(self, 'kwargs', {}),
    #         'request': getattr(self, 'request', None),
    #         'model': 'Library'
    #     }
    #
    #     return context

    def retrieve(self, request, pk=None):
        content = request.GET.get('content')
        tenant = get_current_tenant()
        paras = {}
        if content:
            paras['content'] = content

        queryset_generator = zotero.Zotero(
            tenant.project.zotero_library_id,
            'group',
            tenant.project.zotero_api_key,
        )

        result = queryset_generator.item(pk, **paras)

        return Response(result)
