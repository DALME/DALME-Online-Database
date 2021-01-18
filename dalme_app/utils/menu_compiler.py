import json
import os
from dalme_app.models import Task


class DALMEMenus():
    ''' Class for managing menus throughout the app '''

    def __init__(self, request, state):
        self.dropdowns = self.menu_constructor(request, 'dropdown', 'dropdown_menu_default', state)
        self.sidebar = self.menu_constructor(request, 'sidebar', 'sidebar_menu_default', state)

    def menu_constructor(self, request, constructor_type, template, state):
        '''Builds menus based on an item_constructor_type and a json file describing the menu items.'''
        user_id = request.user.id
        _output = ''
        template = os.path.join('dalme_app', 'config', template + '.json')
        breadcrumb = [i[0] for i in state['breadcrumb']]
        with open(template, 'r') as fp:
            menu = json.load(fp)
        for item in menu:
            if item.get('permissions') is None or self.check_group(request, item['permissions']):
                _output += self.sidebar_menu(breadcrumb, state['sidebar'], **item) if constructor_type == 'sidebar' else self.dropdown_menu(**item)
        if constructor_type == 'dropdown_item':
            _output = self.dropdown_tasks(_output, user_id)
        return [_output]

    def sidebar_menu(self, breadcrumb, sidebar_state, dropdown=False, iconClass=None, text=None, section=False, divider=False,
                     close_dropdown=False, child=False, link=None, itemClass=None, permissions=None):
        if iconClass:
            if ',' in iconClass:
                icons = iconClass.split(',')
                icon = '<span class="fa-stack-container"><i class="fas {} fa-stack-base"></i><i class="fas {} fa-stack-detail"></i></span>'.format(icons[0], icons[1])
            else:
                icon = '<i class="fas fa-fw {}"></i>'.format(iconClass)
        if section:
            currentItem = '<div class="sidebar-heading">{}</div><hr class="sidebar-divider">'.format(text)
        elif divider:
            currentItem = '<hr class="sidebar-divider">'
        elif close_dropdown:
            currentItem = '</li>'
        elif dropdown:
            currentItem = '<li class="nav-item'
            if text in breadcrumb:
                currentItem += ' active'
            currentItem += '">'
            currentItem += '<a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapse{}" aria-expanded="true" \
                            aria-controls="collapse{}">'.format(itemClass, itemClass)
            currentItem += icon
            currentItem += '<span>{}</span></a>'.format(text)
            if text in breadcrumb and not sidebar_state:
                currentItem += '<div id="collapse{}" class="collapse show" aria-labelledby="heading{}" \
                                data-parent="#accordionSidebar">'.format(itemClass, itemClass)
            else:
                currentItem += '<div id="collapse{}" class="collapse" aria-labelledby="heading{}" \
                                data-parent="#accordionSidebar">'.format(itemClass, itemClass)
            currentItem += '<div class="bg-white py-2 collapse-inner rounded">'
        elif child:
            currentItem = '<a class="collapse-item'
            if text in breadcrumb:
                currentItem += ' active'
            currentItem += '" href="{}"'.format(link)
            currentItem += '>' + icon
            currentItem += ' {}</a>'.format(text)
        else:
            currentItem = '<li class="nav-item '
            if itemClass:
                currentItem += itemClass
            if text in breadcrumb:
                currentItem += ' active'
            currentItem += '">'
            currentItem += '<a class="nav-link" href="{}">'.format(link)
            currentItem += icon
            currentItem += '<span>{}</span></a></li>'.format(text)
        return currentItem

    def dropdown_menu(self, link=None, itemClass=None, tooltip=None, iconClass=None, children=None, childrenIconClass=None):
        if link:
            currentItem = '<li class="nav-item dropdown no-arrow topbar-border-left">'
            currentItem += '<a class="nav-link dropdown-toggle" href="{}" id="{}button" role="button" data-toggle="tooltip" \
                            data-placement="bottom" title="{}" data-delay=\'&#123;"show":"1000", "hide":"0"&#125;\'>'.format(link, itemClass, tooltip)
            currentItem += '<i class="{} fa-g"></i></a>'.format(iconClass)
        else:
            currentItem = '<li class="nav-item dropdown no-arrow topbar-border-left" data-toggle="tooltip" data-placement="bottom" \
                           title="{}" data-delay=\'&#123;"show":"1000", "hide":"0"&#125;\'>'.format(tooltip)
            currentItem += '<a class="nav-link dropdown-toggle" href="#" id="{}Dropdown" role="button" data-toggle="dropdown" \
                            aria-haspopup="true" aria-expanded="false">'.format(itemClass)
            currentItem += '<i class="{} fa-g"></i>'.format(iconClass)
            currentItem += '</a><div class="dropdown-menu dropdown-menu-right animated--grow-in" \
                            aria-labelledby="{}Dropdown">'.format(itemClass)
            for child in children:
                if 'divider' in child:
                    currentItem += '<div class="dropdown-divider"></div>'
                else:
                    currentItem += '<a class="dropdown-item" href="{}"'.format(child['link'])
                    if 'action' in child:
                        currentItem += '" onclick="{}"'.format(child['action'])
                    currentItem += '>'
                    if 'iconClass' in child:
                        currentItem += '<i class="{} fa-fw mr-2 text-gray-400"></i>{}</a>'.format(child['iconClass'], child['text'])
                    else:
                        currentItem += '<i class="{} fa-fw mr-2 text-gray-400"></i>{}</a>'.format(childrenIconClass, child['text'])
            currentItem += '</div></li> '
        return currentItem

    def dropdown_tasks(self, wholeMenu, user_id):
        button = ''
        dropmenu = ''
        overdue = False
        counter = False
        if Task.objects.filter(assigned_to=user_id, completed=0).exists():
            tasks = Task.objects.filter(assigned_to=user_id, completed=0)
            counter = tasks.count()
            tasks = tasks[:5]
            for task in tasks:
                dropmenu += '<div class="dropdown-tasks-item">\
                                <div class="dropdown-tasks-text">\
                                    <a href="/tasks/{}" class="dropdown-task-title">{}</a>'.format(task.id, task.title)
                dropmenu += '<div class="dropdown-task-description">{}</div></div>'.format(task.description)
                dropmenu += '<div class="dropdown-tasks-info"><div class="dropdown-tasks-pill">{}</div>'.format(task.task_list)
                if task.due_date:
                    dropmenu += '<div class="dropdown-tasks-pill task-'
                    if task.overdue_status():
                        overdue = True
                        dropmenu += 'over'
                    dropmenu += 'due">Due: {}</div>'.format(task.due_date.strftime('%d-%b-%Y'))
                dropmenu += '</div><div class="dropdown-tasks-buttons"><div class="btn_task_complete" id="{}" onclick="task_set_state({}, {})">\
                            <i class="far fa-square fa-lg"></i></div></div></div>'.format('task_'+str(task.id), task.id, 'False')
        else:
            dropmenu += '<div class="dropdown-tasks-empty">There are currently no tasks in your queue.</div>'
        dropmenu += '<a class="dropdown-tasks-action dropdown-tasks-action-rb" href="{}">{}</a>'.format('/', 'My Tasks')
        dropmenu += '<a class="dropdown-tasks-action" href="{}">{}</a></div></li>'.format('/tasks/', 'All Tasks')

        button = '<li class="nav-item dropdown no-arrow topbar-border-left" data-toggle="tooltip" data-placement="bottom" title="Your task list" \
                  data-delay=\'{"show":"1000", "hide":"0"}\'>'
        button += '<a class="nav-link dropdown-toggle" href="#" id="tasksDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" \
                   aria-expanded="false">'
        button += '<i class="fas fa-tasks fa-fw"></i>'
        if counter:
            if overdue:
                button += '<span class="badge topbar-badge-alert">{}</span>'.format(counter)
            else:
                button += '<span class="badge topbar-badge">{}</span>'.format(counter)
        button += '</a><div class="dropdown-tasks dropdown-menu dropdown-menu-right animated--grow-in" aria-labelledby="tasksDropdown">'
        button += '<div class="dropdown-tasks-header">Your Tasks <div class="dropdown-task-add ml-auto" onclick="create_task()">Add New <i class="fa fa-plus fa-fw"></i></div></div>'
        wholeMenu += button
        wholeMenu += dropmenu
        return wholeMenu

    def check_group(self, request, group_list):
        """ Checks if the current user is a member of any of the groups in the passed list. """
        user_groups = [i.name for i in request.user.groups.all()]
        result = [i for i in user_groups if i in group_list]
        if result or request.user.is_superuser:
            return True
        else:
            return False
