from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView

from dalme_app.models import Source, Source_pages
from dalme_public.filters import SourceFilter
from dalme_public.models import Collection, Home, Set


class SourceList(ListView):
    model = Source
    template_name = 'dalme_public/source_list.html'
    paginate_by = 25
    filterset_class = SourceFilter

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        has_filter = any(
            field in self.request.GET
            for field in [
                'page',
                'date_range_after',
                'date_range_before',
                *self.filterset.filters.keys()
            ]
        )
        context.update({"filterset": self.filterset, 'has_filter': has_filter})
        return context

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs).exclude(
            type__name__in=['Archive', 'File unit']
        ).order_by('name')
        self.filterset = self.filterset_class(self.request.GET, queryset=qs)
        qs = self.filterset.qs.distinct()

        if self.filterset.annotated:
            # Currently necessary because of the inability to eliminate dupes
            # when ordering across the Source - Attribute traversal.
            seen = set()
            filtered = []
            for source in qs:
                if source.pk not in seen:
                    filtered.append(source)
                    seen.add(source.pk)
            qs = filtered

        return qs


class SourceDetail(DetailView):
    model = Source
    template_name = 'dalme_public/source_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_qs = self.object.pages.all().order_by('order')

        # TODO: Refactor this to use the API as much as possible.
        if self.request.GET.get('page'):
            index = int(self.request.GET.get('page')) - 1
            try:
                page = page_qs[index]
            except IndexError:
                raise Http404()
        else:
            page = page_qs.first()
        context.update({
            'page': page,
            'page_id': getattr(page, 'pk', False),
        })

        related = [(page, f"?page={idx}") for idx, page in enumerate(page_qs, 1)]
        has_related = len(related) > 1
        context.update({
            'related': related,
            'has_related': has_related,
        })
        if has_related:
            position = list(page_qs).index(page) + 1
            is_last = position == page_qs.count()
            context.update({
                'previous': None if position == 1 else f"?page={position - 1}",
                'next': None if is_last else f"?page={position + 1}",
            })

        context.update({'transcription_id': None})
        if page:
            context.update({'rights': page.get_rights()})
            source_page = Source_pages.objects.get(source=self.object.id, page=page.id)
            if source_page:
                transcription = source_page.transcription
                if transcription:
                    context.update({'transcription_id': transcription.pk})

        context.update({'parent': self.object.parent})
        return context
