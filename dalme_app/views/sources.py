from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from dalme_app.models import Set, Source, Workflow
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from ._common import DALMEListView, DALMEDetailView
from dalme_api.access_policies import SourceAccessPolicy


@method_decorator(login_required, name='dispatch')
class SourceList(DALMEListView):
    helpers = ['source_forms', 'workflow_module', 'ownership_filter_module']
    includes = ['dam_search_popup']
    form_template = 'form_template_sources'
    editor = 'true'

    def get_page_title(self):
        _class = self.request.GET['class']
        return _class.capitalize().replace('-', ' ')

    def get_breadcrumb(self):
        _class = self.request.GET['class']
        return [('Sources', ''), (_class.capitalize().replace('-', ' '), f'/sources?class={_class}')]

    def get_dt_config(self):
        _class = self.request.GET['class']
        return f'sources_{_class}'


@method_decorator(login_required, name='dispatch')
class SourceDetail(DALMEDetailView):
    model = Source
    template_name = 'dalme_app/source_detail.html'
    comments = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if 'set' in self.request.GET:
            context['workset'] = self.get_workset()

        source_data = {
            'Type': self.object.type.name,
            'Name': self.object.name,
            'Short name': self.object.short_name,
            'List': '<i class="fa fa-check-circle dt_checkbox_true"></i>' if self.object.has_inventory else '<i class="fa fa-times-circle dt_checkbox_false"></i>',
            'Owner': '<a href="/users/{}">{}</a>'.format(self.object.owner.username, self.object.owner.profile.full_name)
        }

        if self.object.parent:
            source_data['Parent'] = '<a href="/sources/{}">{}</a>'.format(str(self.object.parent.id), self.object.parent.name)

        if self.object.type.id == 12 and self.object.primary_dataset:
            source_data['Primary Dataset'] = '<a href="/sets/{}">{}</a>'.format(str(self.object.primary_dataset.id), self.object.primary_dataset.name)

        (attributes, description) = self.get_attributes()

        context.update({
            'can_edit': SourceAccessPolicy().has_permission(self.request, self),
            'source_id': self.object.id,
            'comments_count': self.object.comments.count(),
            'has_inv': False,
            'has_pages': False,
            'has_children': False,
            'has_agents': False,
            'has_places': False,
            'source_data': source_data,
            'attribute_data': attributes,
            'description': description,
            'source_metadata': {
                'ID': str(self.object.id),
                'Created': timezone.localtime(self.object.creation_timestamp).strftime('%d-%b-%Y@%H:%M') + ' by ' + '<a href="/users/{}">{}</a>'.format(self.object.creation_user.username, self.object.creation_user.profile.full_name),
                'Modified': timezone.localtime(self.object.modification_timestamp).strftime('%d-%b-%Y@%H:%M') + ' by ' + '<a href="/users/{}">{}</a>'.format(self.object.modification_user.username, self.object.modification_user.profile.full_name),
            }
        })

        if self.object.has_inventory:
            wf_stages = []
            for k, v in dict(Workflow.PROCESSING_STAGES).items():
                current = 0
                if k == self.object.workflow.stage:
                    current = 1
                wf_stages.append([v, getattr(self.object.workflow, v + '_done'), current])

            context.update({
                'has_inv': True,
                'workflow': self.object.workflow,
                'wf_stages': wf_stages
            })

        tables = []

        if self.object.pages.all().exists():
            title = 'Pages ({})'.format(str(len(self.object.pages.all())))
            folios = self.get_folios()
            tables.append(['pages', 'fa-book-open', title])
            context.update({
                'has_pages': True,
                'folio_count': folios['folio_count'],
                'folio_menu': folios['folio_menu'],
                'folio_list': folios['folio_list']
            })

        if self.object.children.exists():
            title = 'Children ({})'.format(str(len(self.object.children.all())))
            tables.append(['children', 'fa-sitemap', title])
            context.update({
                'has_children': True,
                'children': self.object.children.all().order_by('name')
            })

        if self.object.agents() is not None and len(self.object.agents()) > 0:
            title = 'Agents ({})'.format(str(len(self.object.agents)))
            tables.append(['agents', 'fa-user-friends', title])
            context.update({
                'has_agents': True,
                'agents': self.object.agents
            })

        if self.object.places() is not None and len(self.object.places()) > 0:
            title = 'Places ({})'.format(str(len(self.object.places)))
            tables.append(['places', 'fa-map-marker-alt', title])
            context.update({
                'has_places': True,
                'places': self.object.places
            })

        if tables != []:
            context.update({
                'tables': tables,
                'table_options': {
                    'responsive': 'true',
                    'dom': '''"<'sub-card-header d-flex'<'card-header-title'>fr><'card-body't>"''',
                    'stateSave': 'true',
                    'select': {'style': 'single'},
                    'scrollResize': 'true',
                    'scrollY': '"30vh"',
                    'scrollX': '"100%"',
                    'scrollCollapse': 'true',
                    'deferRender': 'true',
                    'language': {
                        'searchPlaceholder': 'Search',
                        'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
                        },
                    }
            })

        return context

    def get_workset(self):
        workset = Set.objects.get(pk=self.request.GET['set'])
        members = Source.objects.filter(sets__set_id=workset.id)
        current_index = (*members,).index(self.object)
        try:
            previous_id = str(members[current_index - 1].id)
        except (IndexError, AssertionError):
            previous_id = 'none'
        try:
            next_id = str(members[current_index + 1].id)
        except (IndexError, AssertionError):
            next_id = 'none'

        return {
                'workset_id': str(workset.id),
                'name': workset.name,
                'description': workset.description,
                'current': current_index + 1,
                'current_id': str(self.object.id),
                'prev_id': previous_id,
                'next_id': next_id,
                'total': members.count(),
                'endpoint': workset.endpoint,
                'progress': round(workset.workset_progress, 2)
            }

    def get_attributes(self):
        attributes = []
        description = None

        if self.object.attributes is not None:
            for a in self.object.attributes.all():
                label = a.attribute_type.name
                value = str(a)
                if label == 'Description':
                    description = a.value_TXT
                else:
                    attributes.append({'label': label, 'value': value})

        if self.object.inherited is not None:
            for a in self.object.inherited.all():
                label = a.attribute_type.name
                value = str(a)
                attributes.append({'label': label, 'value': value, 'icon': 'fa fa-dna fa-xs'})

        return attributes, description

    def get_breadcrumb(self, *args, **kwargs):
        type = self.get_object().type
        breadcrumb = [('Sources', ''), (type.name + 's', '/sources?class=' + type.short_name + 's')]
        return breadcrumb

    def get_object(self):
        try:
            object = super().get_object()
            return object
        except ObjectDoesNotExist:
            raise Http404

    def get_folios(self):
        folios = self.object.source_pages.all().values(
                pageId=F('page__pk'),
                pageName=F('page__name'),
                pageTranscriptionId=F('transcription__pk'),
                pageTranscriptionVersion=F('transcription__version'),
                pageOrder=F('page__order'),
                pageDamId=F('page__dam_id')
            ).order_by('pageOrder')

        folio_count = len(folios)
        folio_list = []
        folio_menu = '<button class="editor-btn button-border-left" id="btn_prevFolio" \
                     value="" onclick="changeEditorFolio(this.value)" disabled><i class="fa \
                     fa-caret-left fa-fw"></i></button>'

        for i, folio in enumerate(folios):
            folio_dict = {
                'name': folio['pageName'],
                'id': str(folio['pageId']),
                'dam_id': str(folio['pageDamId']),
                'order': str(folio['pageOrder']),
                'tr_id': str(folio['pageTranscriptionId']) or "None",
                'tr_version': folio['pageTranscriptionVersion'] or 0
                }
            folio_list.append(folio_dict)

            if folio_count == 1:
                folio_menu = f'<div class="single_folio">Folio {folio["pageName"]} (1/1)</div>'
            else:
                if i == 0:
                    folio_menu += f'<button id="btn_selectFolio" class="editor-btn button-border-left" data-toggle="dropdown" \
                                    aria-haspopup="true" aria-expanded="false">Folio {folio["pageName"]} (1/{folio_count})</button> \
                                    <div class="dropdown-menu" aria-labelledby="folios"><a class="dropdown-item current-folio" \
                                    href="#" id="0" onclick="changeEditorFolio(this.id)">Folio {folio["pageName"]}</a>'
                else:
                    folio_menu += f'<a class="dropdown-item" href="#" id="{i}" onclick="changeEditorFolio(this.id)">Folio {folio["pageName"]}</a>'

        if folio_count != 1:
            folio_menu += '</div><button class="editor-btn button-border-left" id="btn_nextFolio" value="1" \
                          onclick="changeEditorFolio(this.value)"><i class="fa fa-caret-right fa-fw"></i></button>'

        return {'folio_count': folio_count, 'folio_menu': folio_menu, 'folio_list': folio_list}


def SourceManifest(request, pk):
    context = {}
    source = Source.objects.get(pk=pk)
    context['source'] = source
    context['page_canvases'] = [page.get_canvas() for page in source.pages.all()]
    return render(request, 'dalme_app/source_manifest.html', context)


# @method_decorator(login_required, name='dispatch')
# class SourceDetail(DetailView):
#     model = Source
#     #template_name = 'dalme_app/source_detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         breadcrumb = self.get_breadcrumb()
#         sidebar_toggle = self.request.user.preferences['interface__sidebar_collapsed']
#         context['sidebar_toggle'] = sidebar_toggle
#         state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
#         context['dropdowns'] = dm(self.request, state).dropdowns
#         context['sidebar'] = dm(self.request, state).sidebar
#         page_title = self.object.name
#         context['page_title'] = page_title
#         context['page_chain'] = get_page_chain(breadcrumb, page_title)
#         context['source_id'] = self.object.id
#         return context
#
#     def get_object(self):
#         try:
#             object = super().get_object()
#             return object
#         except ObjectDoesNotExist:
#             raise Http404
#
#     def get_breadcrumb(self, *args, **kwargs):
#         try:
#             parsed_ref = urlparse.urlparse(self.request.META.get('HTTP_REFERER', '/'))
#             s_type = urlparse.parse_qs(parsed_ref.query)['type'][0]
#         except:
#             s_type = 'all'
#         if s_type == 'all':
#             breadcrumb = [('Sources', ''), ('All Sources', '/sources')]
#         elif s_type == 'inventories':
#             breadcrumb = [('Repository', ''), ('Inventories', '/sources?type=inventories')]
#         else:
#             list_label = DT_list.objects.get(short_name=s_type).name
#             breadcrumb = [('Sources', ''), (list_label, '/sources?type='+s_type)]
#         return breadcrumb
