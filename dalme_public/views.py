from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView

from dalme_app.models import Source, Source_pages
from dalme_public.models import Collection, HomePage, Set



def _get_random_source():
    # TODO: Temporary for stubbing data in templates.
    import random
    qs = Source.objects.exclude(type__name__in=['Archive', 'File unit'])
    qs = qs.exclude(attributes__value_STR__contains='Inventory')
    return qs[random.randrange(0, qs.count() - 1)]


def _get_random_inventory():
    # TODO: Temporary for stubbing data in templates.
    import random
    qs = Source.objects.filter(attributes__value_STR__contains='Inventory')
    return qs[random.randrange(0, qs.count() - 1)]


class PublicHome(DetailView):
    model = HomePage
    template_name = 'dalme_public/homepage.html'

    def get_object(self):
        return HomePage.get_solo()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'collections': self.object.collections.all(),
            'object_of_the_month': _get_random_source(),
            'inventory_of_the_month': _get_random_inventory(),
        })
        return context


class CollectionDetail(DetailView):
    model = Collection
    template_name = 'dalme_public/collection_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'sets': self.object.sets.all()})
        return context


class SetDetail(DetailView):
    model = Set
    template_name = 'dalme_public/set_detail.html'


class SourceList(ListView):
    model = Source
    template_name = 'dalme_public/source_list.html'
    paginate_by = 25

    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).exclude(
            type__name__in=['Archive', 'File unit']
        )


class SourceDetail(DetailView):
    model = Source
    template_name = 'dalme_public/source_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        page_qs = self.object.pages.all().order_by('order')

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
            source_page = Source_pages.objects.get(source=self.object.id, page=page.id)
            if source_page:
                transcription = source_page.transcription
                if transcription:
                    context.update({'transcription_id': transcription.pk})

        context.update({'parent': self.object.parent})
        return context
