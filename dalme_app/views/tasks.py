from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.views.generic.base import TemplateView
from dalme_app.utils import DALMEMenus as dm
from dalme_app.models import TaskList, Task
from django.core.exceptions import ObjectDoesNotExist
from ._common import get_page_chain


@method_decorator(login_required, name='dispatch')
class TasksDetail(DetailView):
    model = Task
    template_name = 'dalme_app/task_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        breadcrumb = [('Project', ''), ('Tasks', '/tasks')]
        sidebar_toggle = self.request.user.preferences['interface__sidebar_collapsed']
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
        sidebar_toggle = self.request.user.preferences['interface__sidebar_collapsed']
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
