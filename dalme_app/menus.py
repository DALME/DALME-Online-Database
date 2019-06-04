import json
import os
from dalme_app import functions
from dalme_app.models import Task


def menu_constructor(request, item_constructor, template, state):
    """
    Builds menus based on an item_constructor and a json file describing the menu items.
    Menus are stored in the templates directory, under the menus subdirectory.
    """
    user_id = request.user.id
    _output = ''
    template = os.path.join('dalme_app', 'templates', 'menus', template)
    with open(template, 'r') as fp:
        menu = json.load(fp)
    for item in menu:
        if 'permissions' in item:
            if functions.check_group(request, item['permissions']):
                _output += eval(item_constructor + '(_output,state,**item)')
        else:
            _output += eval(item_constructor + '(_output,state,**item)')
    if item_constructor == 'dropdown_item':
        _output = dropdown_tasks(_output, user_id)
    return [_output]


def sidebar_item(wholeMenu, state, depth=0, text=None, iconClass=None, link=None, counter=None,
                 section=None, children=None, divider=None, itemClass=None, blank=None,
                 permissions=None):
    """ creates menu items for the sidebar """
    if section:
        currentItem = '<div class="sidebar-heading">{}</div><hr class="sidebar-divider">'.format(text)
    elif divider:
        currentItem = '<hr class="sidebar-divider">'
    else:
        if text in state['breadcrumb']:
            currentItem = '<li class="nav-item active">'
        else:
            currentItem = '<li class="nav-item">'
        if children:
            currentItem += '<a class="nav-link collapsed" href="#" data-toggle="collapse" data-target="#collapse{}" aria-expanded="true" \
                            aria-controls="collapse{}">'.format(itemClass, itemClass)
            currentItem += '<i class="fas fa-fw {}"></i>'.format(iconClass)
            currentItem += '<span>{}</span></a>'.format(text)
            if text in state['breadcrumb'] and state['sidebar'] != 'toggled':
                currentItem += '<div id="collapse{}" class="collapse show" aria-labelledby="heading{}" \
                                data-parent="#accordionSidebar">'.format(itemClass, itemClass)
            else:
                currentItem += '<div id="collapse{}" class="collapse" aria-labelledby="heading{}" \
                                data-parent="#accordionSidebar">'.format(itemClass, itemClass)
            currentItem += '<div class="bg-white py-2 collapse-inner rounded">'
            for child in children:
                if 'section' in child:
                    currentItem += '<div class="sidebar-menu-heading">{}</div>'.format(child['text'])
                else:
                    currentItem += '<a class="collapse-item'
                    if child['text'] in state['breadcrumb']:
                        currentItem += ' active'
                    currentItem += '" href="{}"'.format(child['link'])
                    if 'blank' in child:
                        currentItem += ' target="_blank"'
                    currentItem += '><i class="fas fa-fw {}"></i> {}</a>'.format(child['iconClass'], child['text'])
            currentItem += '</div></div></li>'
        else:
            currentItem += '<a class="nav-link" href="{}">'.format(link)
            currentItem += '<i class="fas fa-fw {}"></i>'.format(iconClass)
            currentItem += '<span>{}</span></a></li>'.format(text)
    return currentItem


def dropdown_item(wholeMenu, state, topMenu=None, infoPanel=None, title=None, itemClass=None, iconClass=None,
                  childrenIconClass=None, children=None, text=None, link=None, action=None, divider=None, section=None,
                  counter=None, circleColour=None, moreText=None, moreLink=None, permissions=None, tooltip=None):
    """ creates items for the top right dropdowns """
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


def dropdown_tasks(wholeMenu, user_id):
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
                        <i class="far fa-square fa-lg"></i></div></div></div>'.format('task_'+str(task.id), task.id, 'mark_done')
    else:
        dropmenu += '<div class="dropdown-tasks-empty">There are currently no tasks in your queue.</div>'
    dropmenu += '<a class="dropdown-tasks-action dropdown-tasks-action-rb" href="{}">{}</a>'.format('/tasks/mine', 'My Tasks')
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
    button += '<div class="dropdown-tasks-header">Your Tasks <div class="dropdown-task-add" onclick="create_task()">Add New <i class="fa fa-plus fa-fw"></i></div></div>'
    wholeMenu += button
    wholeMenu += dropmenu
    return wholeMenu
