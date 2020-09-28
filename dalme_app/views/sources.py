from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from dalme_app.utils import DALMEMenus as dm
from dalme_app.models import Set, Source, Workflow
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from ._common import DALMEListView, get_page_chain
from dalme_app.access_policies import SourceAccessPolicy


@method_decorator(login_required, name='dispatch')
class SourceList(DALMEListView):
    helpers = ['source_forms', 'workflow_module', 'ownership_filter_module']
    includes = ['dam_search_popup']
    form_template = 'form_template_sources'
    editor = 'true'

    def get_config(self, *args, **kwargs):
        _class = self.request.GET['class']
        return {
            'page_title': _class.capitalize().replace('-', ' '),
            'dt_config': 'sources_' + _class,
            'breadcrumb': [('Sources', ''), (_class.capitalize().replace('-', ' '), '/sources?class=' + _class)],
            'helpers': self.helpers,
            'includes': self.includes,
            'form_template': self.form_template,
            'editor': self.editor
            }


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


@method_decorator(login_required, name='dispatch')
class SourceDetail(DetailView):
    model = Source

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_edit'] = SourceAccessPolicy().has_permission(self.request, self)
        if 'set' in self.request.GET:
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
            para = {
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
            context['workset'] = para
        breadcrumb = self.get_breadcrumb()
        sidebar_toggle = self.request.user.preferences['interface__sidebar_collapsed']
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        page_title = self.object.name
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        context['source_id'] = self.object.id
        context['comments_count'] = self.object.comments.count()
        has_inv = self.object.has_inventory
        has_pages = self.object.pages.all().exists()
        has_children = self.object.children.exists()
        has_agents = self.object.agents() is not None and len(self.object.agents()) > 0
        has_places = self.object.places() is not None and len(self.object.places()) > 0
        context['has_inv'] = has_inv
        context['has_pages'] = has_pages
        context['has_children'] = has_children
        context['has_agents'] = has_agents
        context['has_places'] = has_places
        if has_inv:
            context['workflow'] = self.object.workflow
            wf_stages = []
            for k, v in dict(Workflow.PROCESSING_STAGES).items():
                current = 0
                if k == self.object.workflow.stage:
                    current = 1
                wf_stages.append([v, getattr(self.object.workflow, v + '_done'), current])
            context['wf_stages'] = wf_stages
        source_data = {
            'Type': self.object.type.name,
            'Name': self.object.name,
            'Short name': self.object.short_name,
            'List': '<i class="fa fa-check-circle dt_checkbox_true"></i>' if has_inv else '<i class="fa fa-times-circle dt_checkbox_false"></i>',
            'Owner': '<a href="/users/{}">{}</a>'.format(self.object.owner.username, self.object.owner.profile.full_name)
        }
        if self.object.parent:
            source_data['Parent'] = '<a href="{}">{}</a>'.format('/sources/'+str(self.object.parent.id), self.object.parent.name)
        if self.object.type.id == 12 and self.object.primary_dataset:
            source_data['Primary Dataset'] = '<a href="{}">{}</a>'.format('/sets/'+str(self.object.primary_dataset.id), self.object.primary_dataset.name)
        context['source_data'] = source_data
        context['source_metadata'] = {
            'ID': str(self.object.id),
            'Created': timezone.localtime(self.object.creation_timestamp).strftime('%d-%b-%Y@%H:%M') + ' by ' + '<a href="/users/{}">{}</a>'.format(self.object.creation_user.username, self.object.creation_user.profile.full_name),
            'Modified': timezone.localtime(self.object.modification_timestamp).strftime('%d-%b-%Y@%H:%M') + ' by ' + '<a href="/users/{}">{}</a>'.format(self.object.modification_user.username, self.object.modification_user.profile.full_name),
        }
        attribute_data = self.get_attributes()
        if attribute_data.get('description', None) is not None:
            context['description'] = attribute_data['description']
        context['attribute_data'] = attribute_data['attributes']
        tables = []
        if has_pages:
            title = 'Pages (' + str(len(self.object.pages.all())) + ')'
            folios = self.get_folios()
            context['folio_count'] = folios['folio_count']
            context['folio_menu'] = folios['folio_menu']
            context['folio_list'] = folios['folio_list']
            tables.append(['pages', 'fa-book-open', title])
        if has_children:
            title = 'Children (' + str(len(self.object.children.all())) + ')'
            context['children'] = self.object.children.all().order_by('name')
            tables.append(['children', 'fa-sitemap', title])
        if has_agents:
            title = 'Agents (' + str(len(self.object.agents)) + ')'
            context['agents'] = self.object.agents
            tables.append(['agents', 'fa-user-friends', title])
        if has_places:
            title = 'Places (' + str(len(self.object.places)) + ')'
            context['places'] = self.object.places
            tables.append(['places', 'fa-map-marker-alt', title])
        if tables != []:
            context['tables'] = tables
            context['table_options'] = {
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
        return context

    def get_attributes(self):
        result = {}
        attributes = []
        if self.object.attributes is not None:
            for a in self.object.attributes.all():
                label = a.attribute_type.name
                value = str(a)
                if label == 'Description':
                    result['description'] = a.value_TXT
                else:
                    attributes.append({'label': label, 'value': value})
        if self.object.inherited is not None:
            for a in self.object.inherited.all():
                label = a.attribute_type.name
                value = str(a)
                attributes.append({'label': label, 'value': value, 'icon': 'fa fa-dna fa-xs'})
        result['attributes'] = attributes
        return result

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
        folios = self.object.pages.all().order_by('order')
        folio_count = len(folios)
        folio_list = []
        if folio_count == 1:
            folio_menu = '<div class="single_folio">Folio {} (1/1)</div>'.format(folios[0].name)
            folio_dict = {
                'name': folios[0].name,
                'id': str(folios[0].id),
                'dam_id': str(folios[0].dam_id),
                'order': str(folios[0].order)
                }
            transcription = self.object.source_pages.all().first().transcription
            folio_dict['tr_id'] = str(transcription.id) if transcription is not None else "None"
            folio_dict['tr_version'] = transcription.version if transcription is not None else 0
            folio_list.append(folio_dict)
        else:
            folio_menu = '<button class="editor-btn button-border-left" id="btn_prevFolio" value="" onclick="changeEditorFolio(this.value)" disabled><i class="fa fa-caret-left fa-fw"></i></button>'
            count = 0
            for f in folios:
                folio_dict = {
                    'name': f.name,
                    'id': str(f.id),
                    'dam_id': str(f.dam_id),
                    'order': str(f.order)
                    }
                transcription = self.object.source_pages.all()[count].transcription
                folio_dict['tr_id'] = str(transcription.id) if transcription is not None else "None"
                folio_dict['tr_version'] = transcription.version if transcription is not None else 0
                if count == 0:
                    folio_menu += '<button id="btn_selectFolio" class="editor-btn button-border-left" data-toggle="dropdown" aria-haspopup="true" \
                                   aria-expanded="false">Folio {} (1/{})</button><div class="dropdown-menu" aria-labelledby="folios">'.format(f.name, folio_count)
                    folio_menu += '<a class="dropdown-item current-folio" href="#" id="0" onclick="changeEditorFolio(this.id)">Folio {}</a>'.format(f.name)
                else:
                    folio_menu += '<a class="dropdown-item" href="#" id="{}" onclick="changeEditorFolio(this.id)">Folio {}</a>'.format(count, f.name)
                count = count + 1
                folio_list.append(folio_dict)
            folio_menu += '</div><button class="editor-btn button-border-left" id="btn_nextFolio" value="1" onclick="changeEditorFolio(this.value)">\
                            <i class="fa fa-caret-right fa-fw"></i></button>'
        return {'folio_count': folio_count, 'folio_menu': folio_menu, 'folio_list': folio_list}


def SourceManifest(request, pk):
    context = {}
    source = Source.objects.get(pk=pk)
    context['source'] = source
    context['page_canvases'] = [page.get_canvas() for page in source.pages.all()]
    return render(request, 'dalme_app/source_manifest.html', context)
