from django.views.generic.base import TemplateView, ContextMixin
from django.views.generic import DetailView
from django.conf import settings
from dalme_app.utils import DALMEMenus as dm
from dalme_app.forms import SearchForm
from django.forms import formset_factory


class DALMEContextMixin(ContextMixin):
    breadcrumb = None
    page_title = None
    comments = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sidebar_toggle = self.request.user.preferences['interface__sidebar_collapsed']
        page_title = self.get_page_title()
        breadcrumb = self.get_breadcrumb()
        state = {
            'breadcrumb': breadcrumb,
            'sidebar': sidebar_toggle
        }

        context.update({
            'api_endpoint': settings.API_ENDPOINT,
            'sidebar_toggle': sidebar_toggle,
            'dropdowns': dm(self.request, state).dropdowns,
            'sidebar': dm(self.request, state).sidebar,
            'page_title': page_title,
            'page_chain': get_page_chain(breadcrumb, page_title),
            'comments': self.comments,
            'form': formset_factory(SearchForm)
        })

        return context

    def get_page_title(self):
        return self.page_title

    def get_breadcrumb(self):
        return self.breadcrumb


class DALMEDetailView(DetailView, DALMEContextMixin):
    template_name = 'dalme_app/generic_detail.html'

    def get_page_title(self):
        return '{}: {}'.format(self.page_title, self.object.name) if self.page_title else self.object.name


class DALMEListView(TemplateView, DALMEContextMixin):
    template_name = 'dalme_app/list-views.html'
    page_title = None
    dt_config = None
    breadcrumb = None
    helpers = None
    includes = None
    editor = 'true'
    form_template = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'config': self.get_dt_config(),
            'helpers': self.helpers,
            'includes': self.includes,
            'form_template': self.form_template,
            'editor': self.editor,
        })

        return context

    def get_dt_config(self):
        return self.dt_config


def get_page_chain(breadcrumb, current=None):
    i_count = len(breadcrumb)
    title = ''
    if current and current != breadcrumb[i_count-1][0]:
        if len(current) > 55:
            current = current[:55] + ' <i class="fa fa-plus-circle fa-fw" data-toggle="tooltip" data-placement="bottom" title="{}"></i> '.format(current)
        for i in breadcrumb:
            if i[1] != '':
                title += '<a href="{}" class="title_link">{}</a>'.format(i[1], i[0])
            else:
                title += i[0]
            title += ' <i class="fa fa-caret-right fa-fw"></i> '
        title += '<span class="title_current">{}</span>'.format(current)
    else:
        c = 0
        while c <= i_count - 1:
            if c == i_count - 1:
                title += '<span class="title_current">{}</span>'.format(breadcrumb[c][0])
            else:
                title += breadcrumb[c][0] + ' <i class="fa fa-caret-right fa-fw"></i> '
            c = c + 1
    return title
