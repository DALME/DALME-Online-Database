import json
import mimetypes
import urllib
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from dalme_app.utils import DALMEMenus as dm
from dalme_app import custom_scripts
from dalme_app.models import (Profile, Content_class, Content_type, DT_list, DT_fields, Page, Attribute_type, Attribute, Tag,
                              Source, Set, TaskList, Task, rs_resource, rs_collection, rs_collection_resource, LocaleReference,
                              LanguageReference, CountryReference, rs_resource_data, Ticket, Workflow, RightsPolicy, get_dam_preview)
from haystack.generic_views import SearchView
import urllib.parse as urlparse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.views import LoginView
from django.utils import timezone


def SessionUpdate(request):
    if not request.is_ajax() or not request.method == 'POST':
        return HttpResponseNotAllowed(['POST'])
    if request.POST['var'] == 'sidebar_toggle':
        if request.session['sidebar_toggle'] == '':
            request.session['sidebar_toggle'] = 'toggled'
        else:
            request.session['sidebar_toggle'] = ''
    return HttpResponse('ok')


def HealthCheck(request):
    return HttpResponse(status=200)


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


def DownloadAttachment(request, path):
    path_tokens = path.split('/')
    original_filename = path_tokens.pop(-1)
    file_path = settings.MEDIA_URL + path
    with urllib.request.urlopen(file_path) as fp:
        response = HttpResponse(fp.read())
    type, encoding = mimetypes.guess_type(original_filename)
    if type is None:
        type = 'application/octet-stream'
    response['Content-Type'] = type
    # response['Content-Length'] = str(os.stat(file_path).st_size)
    if encoding is not None:
        response['Content-Encoding'] = encoding
    # To inspect details for the below code, see http://greenbytes.de/tech/tc2231/
    if u'WebKit' in request.META['HTTP_USER_AGENT']:
        # Safari 3.0 and Chrome 2.0 accepts UTF-8 encoded string directly.
        # filename_header = 'filename=%s' % original_filename.encode('utf-8')
        filename_header = 'filename=%s' % original_filename
    elif u'MSIE' in request.META['HTTP_USER_AGENT']:
        # IE does not support internationalized filename at all.
        # It can only recognize internationalized URL, so we do the trick via routing rules.
        filename_header = ''
    else:
        # For others like Firefox, we follow RFC2231 (encoding extension in HTTP headers).
        filename_header = 'filename*=UTF-8\'\'%s' % urllib.quote(original_filename.encode('utf-8'))
    response['Content-Disposition'] = 'attachment; ' + filename_header
    return response


@method_decorator(login_required, name='dispatch')
class DefaultSearch(SearchView):
    """ Default search view for Haystack"""
    template_name = 'dalme_app/search.html'
    results_per_page = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Search', ''), ('Search Results', '')]
        sidebar_toggle = self.request.session.get('sidebar_toggle', '')
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        page_title = 'Search Results'
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        return context


@method_decorator(login_required, name='dispatch')
class DTListView(TemplateView):
    template_name = 'dalme_app/dtlistview.html'
    breadcrumb = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        config = self.get_config()
        breadcrumb = config['breadcrumb']
        sidebar_toggle = self.request.session.get('sidebar_toggle', '')
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        context['page_title'] = config['page_title']
        context['page_chain'] = get_page_chain(breadcrumb, context['page_title'])
        context['config'] = config['dt_config']
        context['helpers'] = config['helpers']
        context['template'] = config['template']
        return context


@method_decorator(login_required, name='dispatch')
class ModelLists(DTListView):
    template_name = 'dalme_app/models.html'
    dt_editor_options = {'idSrc': '"id"'}
    dt_options = {
        'serverSide': 'true',
        'responsive': 'true',
        'dom': '\'<"sub-card-header-embed d-flex"B<"#fieldsets.btn-group mr-auto"><"btn-group"f>r><"card-body"t><"sub-card-footer"i>\'',
        'stateSave': 'true',
        'select': {'style': 'multi'},
        'scrollResize': 'true',
        'scrollY': '"50vh"',
        'scrollX': '"100%"',
        'deferRender': 'true',
        'scroller': 'true',
        'processing': 'true',
        'language': {
            'searchPlaceholder': 'Search',
            'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
            },
        'rowId': '"id"',
    }
    dt_buttons = [{'extend': 'colvis', 'text': '<i class="fa fa-columns fa-fw"></i>'}]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = self.get_breadcrumb()
        sidebar_toggle = self.request.session.get('sidebar_toggle', '')
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        page_title = self.get_page_title('')
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        model = self.kwargs['model']
        context['model'] = model
        if model == 'content_types':
            qs = Content_class.objects.all().order_by('name')
            parent_class_opt = {i.id: i.name for i in qs}
            context['parent_class'] = {
                'name': 'content class',
                'options': parent_class_opt
            }
        elif model == 'attribute_types':
            qs = Content_type.objects.all().order_by('name')
            parent_class_opt = {i.id: i.name for i in qs}
            context['parent_class'] = {
                'name': 'content type',
                'options': parent_class_opt
            }
        elif model == 'dt_fields':
            context['dt_fieldsets'] = {
                'DT Fields': [3, 4, 5, 6, 7, 8, 9, 10],
                'DTE Fields': [11, 12, 13, 14, 15],
                'Filter Fields': [16, 17, 18, 19]
                }
            qs = DT_list.objects.all().order_by('name')
            parent_class_opt = {i.id: i.name for i in qs}
            context['parent_class'] = {
                'name': 'list',
                'options': parent_class_opt
            }
        list_name = self.get_list_name()
        _list = self.get_list(list_name)
        fields_dict = self.get_fields_dict(_list)
        context['dt_options'] = self.get_dt_options(_list, fields_dict)
        context['dt_editor'] = self.get_dt_editor(_list, fields_dict)
        context['helpers'] = self.get_helpers(_list)
        context['modules'] = self.get_modules()
        return context

    def get_list_name(self, *args, **kwargs):
        return self.kwargs['model']

    def get_breadcrumb(self, *args, **kwargs):
        if self.kwargs['model'] == 'dt_fields':
            breadcrumb = [('Data Models', ''), ('DataTables Fields', '/models/dt_fields')]
        else:
            breadcrumb = [('Data Models', ''), (self.kwargs['model'].replace('_', ' ').title(), '/models/'+self.kwargs['model'])]
        return breadcrumb

    def get_page_title(self, _list, *args, **kwargs):
        model = self.kwargs['model']
        if model == 'content_types':
            page_title = 'Content classes and types'
        elif model == 'attribute_types':
            page_title = 'Content types and attributes'
        elif model == 'dt_fields':
            page_title = 'DataTables lists and fields'
        return page_title

    def get_dt_fields(self, _list, *args, **kwargs):
        model = self.kwargs['model']
        if model == 'content_types':
            dt_field_list = ['id', 'name', 'short_name', 'content_class', 'description', 'attribute_types', 'has_pages', 'parents']
        elif model == 'attribute_types':
            dt_field_list = ['id', 'name', 'short_name', 'description', 'data_type', 'source', 'same_as',
                             'options_list', 'required']
        elif model == 'dt_fields':
            dt_field_list = ['id', 'list', 'field', 'order', 'dt_name', 'orderable', 'visible', 'searchable',
                             'render_exp', 'dt_class_name', 'dt_width', 'dte_name', 'dte_type', 'dte_options',
                             'dte_opts', 'dte_message', 'is_filter', 'filter_type', 'filter_mode', 'filter_options',
                             'filter_lookup']
        return dt_field_list

    def get_dte_fields(self, _list, *args, **kwargs):
        model = self.kwargs['model']
        if model == 'content_types':
            dte_fields = ['name', 'short_name', 'content_class', 'description', 'attribute_types', 'parents', 'r1_inheritance', 'r2_inheritance', 'has_pages', 'has_inventory']
        elif model == 'attribute_types':
            dte_fields = ['name', 'short_name', 'description', 'data_type', 'source', 'same_as', 'options_list', 'required']
        elif model == 'dt_fields':
            dte_fields = ['dt_name', 'order', 'orderable', 'visible', 'searchable', 'render_exp', 'dt_class_name', 'dt_width',
                          'dte_name', 'dte_type', 'dte_options', 'dte_opts', 'dte_message', 'is_filter', 'filter_type',
                          'filter_mode', 'filter_options', 'filter_lookup']
        else:
            dte_fields = None
        return dte_fields

    def get_dte_buttons(self, *args, **kwargs):
        model = self.kwargs['model']
        dte_buttons = []
        if model != 'dt_fields':
            dte_buttons.append({'extend': 'create', 'text': '<i class="fa fa-plus fa-fw dt_menu_icon"></i> Create New'})
            dte_buttons.append({'extend': 'edit', 'text': '<i class="fa fa-pen fa-sm dt_menu_icon"></i> Edit Selected'})
        dte_buttons.append({'action': 'toggle_inline_edit()', 'text': '<i class="fa fa-edit fa-fw dt_menu_icon"></i> Edit Inline',
                            'className': "inline-edit-toggle"})
        dte_buttons.append({'extend': 'remove', 'text': '<i class="fa fa-times fa-fw dt_menu_icon"></i> Delete Selected'})
        dte_buttons.append({'extend': 'selectNone', 'text': '<i class="fa fa-broom fa-fw dt_menu_icon"></i> Clear Selection'})
        return dte_buttons

    def get_modules(self, *args, **kwargs):
        model = self.kwargs['model']
        if model == 'dt_fields':
            module_list = ['fieldsets']
        else:
            module_list = None
        return module_list


@method_decorator(login_required, name='dispatch')
class SourceList(DTListView):
    helpers = ['source_forms', 'workflow_module', 'corpus_filter_module']
    form_template = 'source_form_template'

    def get_config(self, *args, **kwargs):
        _class = self.request.GET['class']
        return {
            'page_title': _class.capitalize().replace('_', ' '),
            'dt_config': 'sources_' + _class,
            'breadcrumb': [('Sources', ''), (_class.capitalize().replace('_', ' '), '/sources?class=' + _class)],
            'helpers': self.helpers,
            'form_template': self.form_template
            }


@method_decorator(login_required, name='dispatch')
class SourceDetail(DetailView):
    model = Source

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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
        sidebar_toggle = self.request.session.get('sidebar_toggle', '')
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
        has_children = self.object.source_set.all().exists()
        has_agents = self.object.agents is not None and len(self.object.agents) > 0
        has_places = self.object.places is not None and len(self.object.places) > 0
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
            title = 'Children (' + str(len(self.object.source_set.all())) + ')'
            context['children'] = self.object.source_set.all().order_by('name')
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
                'scroller': 'true',
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
                    result['description'] = value
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
        try:
            parsed_ref = urlparse.urlparse(self.request.META.get('HTTP_REFERER', '/'))
            s_type = urlparse.parse_qs(parsed_ref.query)['type'][0]
        except:
            s_type = 'all'
        if s_type == 'all':
            breadcrumb = [('Sources', ''), ('All Sources', '/sources')]
        elif s_type == 'inventories':
            breadcrumb = [('Repository', ''), ('Inventories', '/sources?type=inventories')]
        else:
            list_label = DT_list.objects.get(short_name=s_type).name
            breadcrumb = [('Sources', ''), (list_label, '/sources?type='+s_type)]
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
            folio_dict['tr_version'] = transcription.version if transcription.version is not None else 0
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
                folio_dict['tr_version'] = transcription.version if transcription.version is not None else 0
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


@method_decorator(login_required, name='dispatch')
class UserList(DTListView):
    """ Lists users and allows editing and creation of new records via the API """

    def get_config(self, *args, **kwargs):
        return {
            'page_title': 'Users',
            'dt_config': 'users',
            'breadcrumb': [('System', ''), ('Users', '/users/')],
            'helpers': ['user_forms'],
            'template': 'generic_form_template'
            }


@method_decorator(login_required, name='dispatch')
class UserDetail(DetailView):
    model = User
    template_name = 'dalme_app/user_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('System', ''), ('Users', '/users')]
        sidebar_toggle = self.request.session.get('sidebar_toggle', '')
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        page_title = self.object.profile.full_name
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        user_data = {
            'First name': self.object.first_name,
            'Last name': self.object.last_name,
            'User ID': self.object.id,
            'Email': '<a href="mailto:{}">{}</a>'.format(self.object.email, self.object.email),
            'Staff': '<i class="fa fa-check-circle dt_checkbox_true"></i>' if self.object.is_staff else '<i class="fa fa-times-circle dt_checkbox_false"></i>',
            'Superuser': '<i class="fa fa-check-circle dt_checkbox_true"></i>' if self.object.is_superuser else '<i class="fa fa-times-circle dt_checkbox_false"></i>',
            'Active': '<i class="fa fa-check-circle dt_checkbox_true"></i>' if self.object.is_active else '<i class="fa fa-times-circle dt_checkbox_false"></i>',
            'Joined': timezone.localtime(self.object.date_joined).strftime('%d %B, %Y @ %H:%M').lstrip("0").replace(" 0", " "),
            'Last login': timezone.localtime(self.object.last_login).strftime('%d %B, %Y @ %H:%M').lstrip("0").replace(" 0", " "),
            'Groups': ', '.join([i.name for i in self.object.groups.all()])
        }
        context['user_data'] = user_data
        context['image_url'] = self.object.profile.profile_image
        return context

    def get_object(self):
        try:
            object = User.objects.get(username=self.kwargs['username'])
            return object
        except ObjectDoesNotExist:
            raise Http404


@method_decorator(login_required, name='dispatch')
class AsyncTaskList(DTListView):

    def get_config(self, *args, **kwargs):
        return {
            'page_title': 'Asynchronous Tasks',
            'dt_config': 'async_tasks',
            'breadcrumb': [('System', ''), ('Asynchronous Tasks', '/async_tasks')],
            'template': 'generic_form_template'
            }


@method_decorator(login_required, name='dispatch')
class CountryList(DTListView):

    def get_config(self, *args, **kwargs):
        return {
            'page_title': 'Countries',
            'dt_config': 'countries',
            'breadcrumb': [('System', ''), ('Countries', '/countries')],
            'template': 'generic_form_template'
            }


@method_decorator(login_required, name='dispatch')
class LocaleList(DTListView):

    def get_config(self, *args, **kwargs):
        return {
            'page_title': 'Locales',
            'dt_config': 'locales',
            'breadcrumb': [('System', ''), ('Locales', '/locales')],
            'template': 'generic_form_template'
            }


@method_decorator(login_required, name='dispatch')
class RightsList(DTListView):

    def get_config(self, *args, **kwargs):
        return {
            'page_title': 'Rights Policies',
            'dt_config': 'rights',
            'breadcrumb': [('Project', ''), ('Rights Policies', '/rights')],
            'template': 'generic_form_template'
            }


@method_decorator(login_required, name='dispatch')
class RightsDetail(DetailView):
    model = RightsPolicy
    template_name = 'dalme_app/generic_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Project', ''), ('Rights Policies', '/rights')]
        sidebar_toggle = self.request.session.get('sidebar_toggle', '')
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        page_title = 'Policy: ' + self.object.name
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        context['object_class'] = 'Rights Policy'
        context['object_icon'] = 'fas fa-copyright'
        context['comments'] = 'RightsPolicy'
        if self.object.notice_display:
            notice_disp = '<i class="fas fa-check-square"></i>'
        else:
            notice_disp = '<i class="far fa-square"></i>'
        context['attribute_dictionaries'] = ['Rights Notice']
        context['object_attributes'] = {
            'ID': self.object.id,
            'Name': self.object.name,
            'Rights Holder': self.object.rights_holder,
            'Rights Status': self.object.get_rights_status_display(),
            'Rights': self.object.rights,
            'Notice Display': notice_disp,
            'Rights Notice': json.loads(self.object.rights_notice),
            'Licence': self.object.licence,
            'Attachment': '<a href="/download/{}">{}</a></div></div>'.format(self.object.attachments.file, self.object.attachments.filename)
        }
        return context

    def get_object(self):
        try:
            object = RightsPolicy.objects.get(pk=self.kwargs['pk'])
            return object
        except ObjectDoesNotExist:
            raise Http404


@method_decorator(login_required, name='dispatch')
class LanguageList(DTListView):

    def get_config(self, *args, **kwargs):
        return {
            'page_title': 'Languages',
            'dt_config': 'languages',
            'breadcrumb': [('System', ''), ('Languages', '/languages')],
            'template': 'generic_form_template'
            }


@method_decorator(login_required, name='dispatch')
class ImageList(DTListView):

    def get_config(self, *args, **kwargs):
        return {
            'page_title': 'DAM Images',
            'dt_config': 'images',
            'breadcrumb': [('DAM Images', '/images')],
            'helpers': ['preview_module'],
            'template': 'generic_form_template'
            }
    # breadcrumb = [('DAM Images', '/images')]
    # list_name = 'images'
    # dt_editor_options = {'idSrc': '"id"'}
    # dte_field_list = ['field8', 'field79', 'field12', 'field3', 'collections']
    # dt_options = {
    #     'pageLength': 25,
    #     'paging': 'true',
    #     'responsive': 'true',
    #     'fixedHeader': 'true',
    #     'dom': '\'<"card-table-header"B<"btn-group ml-auto"f>r><"#filters-container.collapse.clearfix"><"panel-container"<"panel-left"t>><"sub-card-footer"ip>\'',
    #     'serverSide': 'true',
    #     'stateSave': 'true',
    #     'select': {'style': 'multi'},
    #     'deferRender': 'true',
    #     'rowId': '"id"',
    #     'processing': 'true',
    #     'language': {
    #         'searchPlaceholder': 'Search',
    #         'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
    #         },
    #     # 'order': '[[ 1, "asc" ]]'
    #     }
    # module_list = ['filters', 'preview']

    # def get_dte_buttons(self, *args, **kwargs):
    #     dte_buttons = []
    #     if self.request.user.has_perm('dalme_app.change_rs_resource'):
    #         dte_buttons.append({'extend': 'edit', 'text': '<i class="fa fa-pen fa-sm dt_menu_icon"></i> Edit Selected', 'formTitle': 'Edit Image Information'})
    #         dte_buttons.append({'action': 'toggle_inline_edit()', 'text': '<i class="fa fa-edit fa-fw dt_menu_icon"></i> Edit Inline', 'className': "inline-edit-toggle"})
    #     if self.request.user.has_perm('dalme_app.delete_rs_resource'):
    #         dte_buttons.append({'extend': 'remove', 'text': '<i class="fa fa-times fa-fw dt_menu_icon"></i> Delete Selected', 'formTitle': 'Delete Image',
    #                             'formMessage': 'Are you sure you wish to remove this image from the DAM? This action cannot be undone.'})
    #     if self.request.user.has_perm('dalme_app.add_source'):
    #         dte_buttons.append({'extend': 'selectAll', 'text': '<i class="fa fa-check-double fa-fw dt_menu_icon"></i> Select All'})
    #         dte_buttons.append({'extend': 'selectNone', 'text': '<i class="fa fa-broom fa-fw dt_menu_icon"></i> Clear Selection'})
    #         dte_buttons.append({'extend': 'selected', 'action': 'create_source_from_selected()', 'text': '<i class="fa fa-plus-square fa-fw dt_menu_icon"></i> Create Source from Selection'})
    #     return dte_buttons


@method_decorator(login_required, name='dispatch')
class ImageDetail(DetailView):
    model = rs_resource
    template_name = 'dalme_app/image_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('DAM Images', '/images')]
        sidebar_toggle = self.request.session.get('sidebar_toggle', '')
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        page_title = 'DAM Image ' + str(self.object.ref)
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        image_data = {
            'DAM Id': self.object.ref,
            'Created': timezone.localtime(self.object.creation_date).strftime('%d-%b-%Y@%H:%M'),
            'Creator': rs_user.objects.get(ref=self.object.created_by).fullname if rs_user.objects.filter(ref=self.object.created_by).exists() else self.object.created_by,
            'Record modified': timezone.localtime(self.object.modified).strftime('%d-%b-%Y@%H:%M'),
            'File modified': timezone.localtime(self.object.file_modified).strftime('%d-%b-%Y@%H:%M'),
            'Filesize': self.object.file_size,
            'Image?': '<i class="fa fa-check-circle dt_checkbox_true"></i>' if self.object.has_image else '<i class="fa fa-times-circle dt_checkbox_false"></i>'
        }
        context['image_data'] = image_data
        tables = []
        if rs_resource_data.objects.filter(resource=self.object.ref).order_by('resource_type_field').exists():
            attribute_data = []
            attributes = rs_resource_data.objects.filter(resource=self.object.ref).order_by('resource_type_field')
            for a in attributes:
                value = a.value
                name = a.resource_type_field.name
                label = a.resource_type_field.title
                d = {
                    'name': name,
                    'label': label,
                    'value': value,
                }
                attribute_data.append(d)
            context['attribute_data'] = attribute_data
        if rs_collection_resource.objects.filter(resource=self.object.ref).exists():
            collections = []
            col_list = rs_collection_resource.objects.filter(resource=self.object.ref)
            for col in col_list:
                path = ''
                if col.collection.theme:
                    path += col.collection.theme
                    if col.collection.theme2:
                        path += ' ≫ '+col.collection.theme2
                        if col.collection.theme3:
                            path += ' ≫ '+col.collection.theme3
                d = {
                    'id': col.collection.ref,
                    'name': col.collection.name,
                    'creator': rs_user.objects.get(ref=col.collection.user).fullname if rs_user.objects.filter(ref=col.collection.user).exists() else col.collection.user,
                    'path': path
                }
                collections.append(d)
            context['collections'] = collections
            tables.append(['collections', 'fa-th-large', 'Collections'])
        if tables != []:
            context['tables'] = tables
            context['table_options'] = {
                'responsive': 'true',
                'dom': '''"<'sub-card-header d-flex'<'card-header-title'>fr><'card-body't>"''',
                'stateSave': 'true',
                'select': {'style': 'single'},
                'scrollY': 150,
                'deferRender': 'true',
                'scroller': 'true',
                'language': {
                    'searchPlaceholder': 'Search',
                    'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
                    },
                }
        context['image_url'] = get_dam_preview(self.object.ref)
        return context

    def get_object(self):
        try:
            object = super().get_object()
            return object
        except ObjectDoesNotExist:
            raise Http404


@method_decorator(login_required, name='dispatch')
class Index(TemplateView):
    template_name = 'dalme_app/index.html'
    default_cards = ['/dalme_app/cards/counter_articles.html',
                     'dalme_app/cards/counter_assets.html',
                     'dalme_app/cards/counter_inventories.html']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Dashboard', '')]
        if self.request.session.get('sidebar_toggle') is not None:
            sidebar_toggle = self.request.session.get('sidebar_toggle', '')
        else:
            sidebar_toggle = ''
            self.request.session['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['sidebar_toggle'] = sidebar_toggle
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        page_title = 'Dashboard'
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        return context


def PageManifest(request, pk):
    context = {}
    page = Page.objects.get(pk=pk)
    context['page'] = page
    context['canvas'] = page.get_canvas()
    return render(request, 'dalme_app/page_manifest.html', context)


@method_decorator(login_required, name='dispatch')
class SetList(DTListView):

    def get_config(self, *args, **kwargs):
        return {
            'page_title': 'Sets',
            'dt_config': 'sets',
            'breadcrumb': [('Project', ''), ('Sets', '/sets')],
            'template': 'generic_form_template'
            }


@method_decorator(login_required, name='dispatch')
class SetsDetail(DetailView):
    model = RightsPolicy
    template_name = 'dalme_app/set_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Project', ''), ('Sets', '/sets')]
        sidebar_toggle = self.request.session.get('sidebar_toggle', '')
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        page_title = self.object.name
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        context['set'] = self.object
        context['comments_count'] = self.object.comments.count()
        members = self.object.members.all()
        context['members'] = members
        tables = ['members', 'fa-plus-square', 'Set Members ({})'.format(members.count())]
        if tables != []:
            context['tables'] = tables
            context['table_options'] = {
                'responsive': 'true',
                'dom': '''"<'sub-card-header d-flex'<'card-header-title'>Bfr><'card-body't>"''',
                'stateSave': 'true',
                'select': {'style': 'multi'},
                'scrollY': '''"calc(100vh - 600px)"''',
                'deferRender': 'true',
                'scroller': 'true',
                'rowId': '"id"',
                'language': {
                    'searchPlaceholder': 'Search',
                    'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
                },
                'buttons': "[{text: '<i class=\"fa fa-trash-alt fa-fw\"></i>', action: function (e, dt, node, config) {delete_set_members(dt, \"" + str(self.object.id) + "\")}, className: \"align-self-end\"}]"
            }
        return context

    def get_object(self):
        try:
            object = Set.objects.get(pk=self.kwargs['pk'])
            return object
        except ObjectDoesNotExist:
            raise Http404


@method_decorator(login_required, name='dispatch')
class SetsRedirect(View):
    def get(self, request, *args, **kwargs):
        workset = get_object_or_404(Set, pk=kwargs['pk'])
        members = Source.objects.filter(sets__set_id=workset.id)
        try:
            current = members.filter(sets__workset_done=False)[0]
        except IndexError:
            current = members[-1]
        url = '/{}/{}/?set={}'.format(workset.endpoint, current.id, workset.id)
        return HttpResponseRedirect(url)


@method_decorator(login_required, name='dispatch')
class Scripts(TemplateView):
    template_name = 'dalme_app/scripts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Scripts', '')]
        sidebar_toggle = self.request.session.get('sidebar_toggle', '')
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['sidebar_toggle'] = sidebar_toggle
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        context['scripts'] = custom_scripts.get_script_menu()
        page_title = 'Custom Scripts'
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        if self.request.GET.get('s') is not None:
            context['output'] = eval('custom_scripts.'+self.request.GET['s']+'(self.request)')
        return context


@method_decorator(login_required, name='dispatch')
class TicketDetail(DetailView):
    model = Ticket
    template_name = 'dalme_app/ticket_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Project', ''), ('Issue Tickets', '/tickets')]
        sidebar_toggle = self.request.session.get('sidebar_toggle', '')
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        page_title = 'Ticket #'+str(self.object.id)
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        context['ticket'] = self.object
        return context

    def get_object(self):
        try:
            object = super().get_object()
            return object
        except ObjectDoesNotExist:
            raise Http404


@method_decorator(login_required, name='dispatch')
class TicketList(DTListView):

    def get_config(self, *args, **kwargs):
        return {
            'page_title': 'Issue Tickets',
            'dt_config': 'tickets',
            'breadcrumb': [('Project', ''), ('Issue Tickets', '/tickets')],
            'template': 'generic_form_template'
            }


@method_decorator(login_required, name='dispatch')
class TasksDetail(DetailView):
    model = Task
    template_name = 'dalme_app/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Project', ''), ('Tasks', '/tasks')]
        sidebar_toggle = self.request.session.get('sidebar_toggle', '')
        context['sidebar_toggle'] = sidebar_toggle
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        page_title = 'Task #'+str(self.object.id)+' ('+self.object.task_list.name+')'
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        context['task'] = self.object
        return context

    def get_object(self):
        try:
            object = super().get_object()
            return object
        except ObjectDoesNotExist:
            raise Http404


@method_decorator(login_required, name='dispatch')
class TasksList(TemplateView):
    template_name = 'dalme_app/tasks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Project', ''), ('Tasks', '/tasks')]
        sidebar_toggle = self.request.session.get('sidebar_toggle', '')
        state = {'breadcrumb': breadcrumb, 'sidebar': sidebar_toggle}
        context['sidebar_toggle'] = sidebar_toggle
        context['dropdowns'] = dm(self.request, state).dropdowns
        context['sidebar'] = dm(self.request, state).sidebar
        page_title = 'Task Manager'
        context['page_title'] = page_title
        context['page_chain'] = get_page_chain(breadcrumb, page_title)
        # Superusers see all lists
        if self.request.user.is_superuser:
            lists = TaskList.objects.all().order_by('group', 'name')
        else:
            lists = TaskList.objects.filter(group__in=self.request.user.groups.all()).order_by('group', 'name')
        list_count = lists.count()
        # superusers see all lists, so count shouldn't filter by just lists the admin belongs to
        if self.request.user.is_superuser:
            task_count = Task.objects.filter(completed=0).count()
        else:
            task_count = Task.objects.filter(completed=0).filter(task_list__group__in=self.request.user.groups.all()).count()
        context['lists'] = lists
        context['list_count'] = list_count
        context['task_count'] = task_count
        context['tables'] = [
            ['lists', 'fa-tasks', 'Lists', {
                'ajax': '"/api/tasklists/?format=json"',
                'serverSide': 'true',
                'responsive': 'true',
                'dom': '''"<'sub-card-header d-flex'<'card-header-title'><'dt-btn-group'>r><'card-body't><'sub-card-footer'i>"''',
                'select': {'style': 'single'},
                'scrollResize': 'true',
                'scrollY': '"82vh"',
                'scrollX': '"100%"',
                'deferRender': 'true',
                'scroller': 'true',
                'rowId': '"id"',
                'order': '[ 1, "asc" ]',
                'rowGroup': '{dataSrc: \'group\'}',
                'columnDefs': [
                      {
                          'title': '"List"',
                          'targets': 0,
                          'data': '"name"'
                      },
                      {
                          'title': '"Group"',
                          'targets': 1,
                          'data': '"group"',
                          "visible": 'false'
                      }
                      ]
                }
             ],
            ['tasks', 'fa-calendar-check', 'Tasks', {
                'ajax': '"/api/tasks/?format=json"',
                'serverSide': 'true',
                'responsive': 'true',
                'dom': '''"<'sub-card-header d-flex'<'card-header-title'><'dt-btn-group'>fr><'card-body't><'sub-card-footer'i>"''',
                'select': {'style': 'single'},
                'scrollResize': 'true',
                'scrollY': '"82vh"',
                'scrollX': '"100%"',
                'deferRender': 'true',
                'scroller': 'true',
                'language': {
                    'searchPlaceholder': 'Search',
                    'processing': '<div class="spinner-border ml-auto mr-auto" role="status"><span class="sr-only">Loading...</span></div>'
                    },
                'rowId': '"id"',
                'columnDefs': [
                      {
                          'title': '"Task"',
                          'targets': 0,
                          'data': '"task"',
                          'visible': 1,
                          "orderData": '[ 6, 7 ]',
                          'searchable': 0
                      },
                      {
                          'title': '"Dates"',
                          'targets': 1,
                          'data': '"dates"',
                          'visible': 1,
                          "orderData": '[ 5, 7 ]',
                          'searchable': 0
                      },
                      {
                          'title': '"Assigned to"',
                          'targets': 2,
                          'data': '"assigned_to"',
                          'visible': 1,
                          'searchable': 0
                      },
                      {
                          'title': '"Attachments"',
                          'targets': 3,
                          'data': '"attachments"',
                          'visible': 1,
                          'orderable': 0,
                          'searchable': 0,
                      },
                      {
                          'title': '"Done"',
                          'targets': 4,
                          'data': '"completed"',
                          'render': 'function ( data, type, row, meta ) {return data == true ? \'<i class="fa fa-check-circle dt_checkbox_true"></i>\' : \'<i class="fa fa-times-circle dt_checkbox_false"></i>\';}',
                          'className': '"td-center"',
                          'width': '"19px"',
                          'visible': 1,
                          'searchable': 0
                      },
                      {
                          'title': '"Due date"',
                          'targets': 5,
                          'data': '"due_date"',
                          'visible': 0,
                      },
                      {
                          'title': '"Title"',
                          'targets': 6,
                          'data': '"title"',
                          'visible': 0,
                      },
                      {
                          'title': '"Created"',
                          'targets': 7,
                          'data': '"creation_timestamp"',
                          'visible': 0,
                      },
                      {
                          'title': '"Description"',
                          'targets': 8,
                          'data': '"description"',
                          'visible': 0,
                      }
                  ]
                }
             ]
        ]
        return context


class DalmeLogin(LoginView):
    """ Overwrites LoginView method to allow users to be redirected accross subdomains on login """

    def get_redirect_url(self):
        """Return the user-originating redirect URL"""
        redirect_to = self.request.POST.get(
            self.redirect_field_name,
            self.request.GET.get(self.redirect_field_name, '')
        )
        return redirect_to
