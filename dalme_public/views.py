from django.http import Http404
from django.views.generic import DetailView, ListView

from dalme_app.models import Source, Source_pages


class SourceList(ListView):
    model = Source
    template_name = 'dalme_public/source_list.html'
    paginate_by = 25


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

        related = [
            (page, f"?page={idx}") for idx, page in enumerate(page_qs, 1)
        ]
        context.update({'related': related})

        context.update({'transcription': None})
        if page:
            source_page = Source_pages.objects.get(source=self.object.id, page=page.id)
            if source_page:
                transcription = source_page.transcription
                if transcription:
                    split = transcription.transcription.split('\n')
                    context.update({'transcription': split})

        context.update({
            'parent': self.object.parent,
            'type': self.object.type,
        })
        return context
