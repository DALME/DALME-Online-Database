from dalme_app import functions
from django.core.urlresolvers import reverse

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
        ['fa-tasks', 'dropdown-tasks2', [
                ['1', reverse('todo-lists'), 'fa-check-circle', 'General Tasks'],
                ['1', reverse('todo-mine'), 'fa-check-square-o', 'My Tasks'],

            ]

        ],
        ['fa-gears', 'dropdown-dev', [
                ['1', '/dashboard/list/errors', 'fa-medkit', 'Error codes'],
                ['divider'],
                ['0', '#', 'fa-list-alt', 'UI Reference:'],
                ['1', '/dashboard/UIref/dash_demo', 'fa-play-circle-o', 'Dashboard Content'],
                ['1', '/dashboard/UIref/panels-wells', 'fa-play-circle-o', 'Panels and Wells'],
                ['1', '/dashboard/UIref/buttons', 'fa-play-circle-o', 'Buttons'],
                ['1', '/dashboard/UIref/notifications', 'fa-play-circle-o', 'Notifications'],
                ['1', '/dashboard/UIref/typography', 'fa-play-circle-o', 'Typography'],
                ['1', '/dashboard/UIref/icons', 'fa-play-circle-o', 'Icons'],
                ['1', '/dashboard/UIref/grid', 'fa-play-circle-o', 'Grid'],
                ['1', '/dashboard/UIref/tables', 'fa-play-circle-o', 'Tables'],
                ['1', '/dashboard/UIref/flot', 'fa-play-circle-o', 'Flot Charts'],
                ['1', '/dashboard/UIref/morris', 'fa-play-circle-o', 'Morris.js Charts'],
                ['1', '/dashboard/UIref/forms', 'fa-play-circle-o', 'Forms'],
            ]
        ],
        ['fa-user', 'dropdown-user', [
                ['1', '#', 'fa-user', 'Profile'],
                ['1', '#', 'fa-gear', 'Settings'],
                ['divider'],
                ['1', '/logout/', 'fa-sign-out', logout],
            ]
        ],
    ]

    results = []
    _output = ''

    for item in dropdowns:
        _output = '<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#"><i class="fa ' + item[0] + ' fa-fw"></i> <i class="fa fa-caret-down"></i></a><ul class="dropdown-menu ' + item[1] + '">'
        for menu in item[2]:
            if menu[0] == 'divider':
                _output = _output + '<li class="divider"></li>'

            elif menu[0] == '0':
                _output = _output + '<li class="dropdown-section"><i class="fa ' + menu[2] + ' fa-fw"></i> ' + menu[3] + '</li>'

            elif menu[0] == '1':
                _output = _output + '<li><a href="' + menu[1] + '"><i class="fa ' + menu[2] + ' fa-fw"></i> ' + menu[3] + '</a></li>'


        _output = _output + '</ul></li>'
        results.append(_output)

    return results
