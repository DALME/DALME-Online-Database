from dalme_app import functions
from django.core.urlresolvers import reverse
from todo.models import Item, List, Comment
from django.contrib.auth.models import User



def sidebar_menu():
    """ creates the sidebar menu """

    #this is an example of how a full, hierarchical menu would work
    #the list includes these field : ['level', 'name', 'href', 'CSSicon', 'hasChildren', 'isLastSubmenu'], e.g.:
    #menu = [
        #['1', 'Top Level Test', '#', 'fa-question-circle', 'Yes', ''],
        #    ['2', 'Second level 1', '#', 'fa-info-circle', 'No', ''],
        #    ['2', 'Second level 2', '#', 'fa-info-circle', 'Yes', ''],
        #        ['3', 'Third level 1', '#', '', 'No', ''],
        #        ['3', 'Third level 2', '#', '', 'No', 'Last'],
        #    ['2', 'Second level 3', '#', 'fa-info-circle', 'No', 'Last'],
        #['1', 'Top Level Test 2', '#', 'fa-money', 'No', ''],
        #]
    inv_counter = str(functions.get_count('inventories'))
    obj_counter = str(functions.get_count('objects'))
    menu = [
            ['0', 'section-first', 'Modules', 'fa-th'],
            ['1c', 'Inventories', '/dashboard/list/inventories', 'fa-list', 'No', '', inv_counter],
            ['1c', 'Objects', '/dashboard/list/objects', 'fa-beer', 'No', '', obj_counter],
            ['0', 'section', 'Tools', 'fa-wrench'],
            ['1', 'Bookmarks', '#', 'fa-bookmark', 'Yes', ''],
                ['2', 'Wiki', 'http://dighist.fas.harvard.edu/projects/DALME/wiki', 'fa-book', 'No', ''],
                ['2', 'DAM', 'http://dighist.fas.harvard.edu/projects/DALME/dam', 'fa-image', 'No', 'Last'],
            ['1', 'Admin', '#', 'fa-group', 'Yes', ''],
                ['2', 'Users', '#', 'fa-user', 'No', ''],
                ['2', 'Website', '#', 'fa-globe', 'No', 'Last'],
            ['1', 'Background Tasks', '/dashboard/list/tasks', 'fa-tasks', 'No', ''],
            ]


    results = []
    _output = ''
    submenu = 0

    for item in menu:
        if item[0] == '0':
            _output = '<li class="sidebar-' + item[1] + '"><i class="fa ' + item[3] +' fa-fw"></i> ' + item[2] + '</li>'

        else:
            if item[4] == 'No':
                if item[0] == '1c':
                    _output = '<li><a href="' + item[2] + '"><i class="fa ' + item[3] +' fa-fw"></i> ' + item[1] + '<div class="menu-counter">' + item[6] + '</div></a></li>'
                else:
                    _output = '<li><a href="' + item[2] + '"><i class="fa ' + item[3] +' fa-fw"></i> ' + item[1] + '</a></li>'

                if item[5] == 'Last' and submenu == 1:
                    _output = _output + '</ul></li></ul></li>'
                    submenu = 0

                elif item[5] == 'Last' and submenu == 0:
                    _output = _output + '</ul></li>'

                else:
                    _output = _output + '</li>'

            elif item[4] == 'Yes':
                _output = '<li><a href="' + item[2] + '"><i class="fa ' + item[3] +' fa-fw"></i> ' + item[1] + '<span class="fa arrow"></span></a>'

                if item[0] == '1' or item[0] == '1c':
                    _output = _output + '<ul class="nav nav-second-level">'

                elif item[0] == '2':
                    _output = _output + '<ul class="nav nav-third-level">'

                elif item[0] == '3':
                    _output = _output + '<ul class="nav nav-fourth-level">'

                elif item[0] == '4':
                    _output = _output + '<ul class="nav nav-fifth-level">'

                if item[5] == 'Last':
                    submenu = 1

        results.append(_output)

    return results

def dropdowns(username):
    """ creates the top right dropdowns """
    logout = 'Logout ' + username

    dropdowns = [
        ['fa fa-tasks', 'dropdown-task-list', [
                ['1', reverse('todo-lists'), 'fa fa-plus-circle', 'Add New Task'],
                ['divider'],
                ['1', reverse('todo-lists'), 'fa fa-info-circle', 'Manage Task Lists'],
                ['1', reverse('todo-lists'), 'fa fa-check-circle', 'View Tasks Log'],
                ['divider'],
                ['0', '#', 'fa fa-star', 'My Tasks:'],
            ]

        ],
        ['fa fa-gears', 'dropdown-dev', [
                ['1', '/dashboard/list/errors', 'fa fa-medkit', 'Error codes'],
                ['divider'],
                ['0', '#', 'fa fa-list-alt', 'UI Reference:'],
                ['1', '/dashboard/UIref/dash_demo', 'fa fa-dot-circle-o', 'Dashboard Content'],
                ['1', '/dashboard/UIref/panels-wells', 'fa fa-dot-circle-o', 'Panels and Wells'],
                ['1', '/dashboard/UIref/buttons', 'fa fa-dot-circle-o', 'Buttons'],
                ['1', '/dashboard/UIref/notifications', 'fa fa-dot-circle-o', 'Notifications'],
                ['1', '/dashboard/UIref/typography', 'fa fa-dot-circle-o', 'Typography'],
                ['1', '/dashboard/UIref/icons', 'fa fa-dot-circle-o', 'Icons'],
                ['1', '/dashboard/UIref/grid', 'fa fa-dot-circle-o', 'Grid'],
                ['1', '/dashboard/UIref/tables', 'fa fa-dot-circle-o', 'Tables'],
                ['1', '/dashboard/UIref/flot', 'fa fa-dot-circle-o', 'Flot Charts'],
                ['1', '/dashboard/UIref/morris', 'fa fa-dot-circle-o', 'Morris.js Charts'],
                ['1', '/dashboard/UIref/forms', 'fa fa-dot-circle-o', 'Forms'],
            ]
        ],
        ['fa fa-user', 'dropdown-user', [
                ['1', '#', 'fa fa-user', 'Profile'],
                ['1', '#', 'fa fa-gear', 'Settings'],
                ['divider'],
                ['1', '/logout/', 'fa fa-sign-out', logout],
            ]
        ],
    ]

    user_id = User.objects.get(username=username).pk
    tasks = Item.objects.filter(assigned_to=user_id, completed=False).order_by('-created_date')[:5]
    for i in tasks:
        task_icon = functions.get_task_icon(i.list_id)
        task_url = '/dashboard/tasks/task/' + str(i.id)
        creator_id = i.created_by_id
        task_creator = User.objects.get(id=creator_id).username
        date_created = i.created_date.strftime('%a, %-d %b, %Y')
        date_due = i.due_date.strftime('%a, %-d %b, %Y')
        task_item = ['2', task_url, task_icon, i.title, str(i.id), date_created, date_due, task_creator]
        dropdowns[0][2].append(task_item)

    close_tasks = ['3', reverse('todo-mine'), 'See All']
    dropdowns[0][2].append(close_tasks)

    results = []
    _output = ''

    for item in dropdowns:
        if item[0] == 'fa-tasks':
            _output = '<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#"><i class="' + item[0] + ' fa-fw"></i> <i class="fa fa-caret-down"></i></a><ul class="dropdown-menu ' + item[1] + '"><form action="" method="POST">'

        else:
            _output = '<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#"><i class="' + item[0] + ' fa-fw"></i> <i class="fa fa-caret-down"></i></a><ul class="dropdown-menu ' + item[1] + '">'

        for menu in item[2]:
            if menu[0] == 'divider':
                _output = _output + '<li class="divider"></li>'

            elif menu[0] == '0':
                _output = _output + '<li class="dropdown-section"><i class="' + menu[2] + ' fa-fw"></i> ' + menu[3] + '</li>'

            elif menu[0] == '1':
                _output = _output + '<li><a href="' + menu[1] + '"><i class="' + menu[2] + ' fa-fw"></i> ' + menu[3] + '</a></li>'

            elif menu[0] == '2':
                _output = _output + '<li><a href="' + menu[1] + '"><div><input class="dropdown-checkbox" type="checkbox" name="mark_done" value="' + menu[4]+ '" id="mark_done_' + menu[4] + '">' + menu[3] + '<span class="pull-right text-muted"><em>Due: ' + menu[6] + '</em></span></div><div><em>Created: ' + menu[5] + ' By: ' + menu[7] + '</em></div></a></li>'

            elif menu[0] == '3':
                _output = _output + '<li class="divider"></li><li><a class="text-center" href="' + menu[1] + '"><strong>' + menu[2] + ' </strong><i class="fa fa-angle-right"></i></a></li>'


        if dropdowns[0][0] == 'fa fa-tasks':
            _output = _output + '</form></ul></li>'
        else:
            _output = _output + '</ul></li>'

        results.append(_output)

    return results
