from dalme_app import functions

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

def dropdowns():
    """ creates the top right dropdowns """

    dropdowns = [
        ['fa-gears', [
                ['1', '/dashboard/list/errors', 'fa-medkit', 'Error codes'],
                ['divider'],
                ['0', '#', 'fa-list-alt', 'UI Reference:'],
                ['2', '/dashboard/UIref/dash_demo', '', 'Dashboard Content'],
                ['2', '/dashboard/UIref/panels-wells', '', 'Panels and Wells'],
                ['2', '/dashboard/UIref/buttons', '', 'Buttons'],
                ['2', '/dashboard/UIref/notifications', '', 'Notifications'],
                ['2', '/dashboard/UIref/typography', '', 'Typography'],
                ['2', '/dashboard/UIref/icons', '', 'Icons'],
                ['2', '/dashboard/UIref/grid', '', 'Grid'],
                ['2', '/dashboard/UIref/tables', '', 'Tables'],
                ['2', '/dashboard/UIref/flot', '', 'Flot Charts'],
                ['2', '/dashboard/UIref/morris', '', 'Morris.js Charts'],
                ['2', '/dashboard/UIref/forms', '', 'Forms'],
            ]
        ],
    ]

    results = []
    _output = ''

    for item in dropdowns:
        _output = '<li class="dropdown"><a class="dropdown-toggle" data-toggle="dropdown" href="#"><i class="fa ' + item[0] + ' fa-fw"></i> <i class="fa fa-caret-down"></i></a><ul class="dropdown-menu dropdown-user">'
        for menu in item[1]:
            if menu[0] == 'divider':
                _output = _output + '<li class="divider"></li>'

            elif menu[0] == '0':
                _output = _output + '<li class="dropdown-section"><i class="fa ' + menu[2] + ' fa-fw"></i> ' + menu[3] + '</li>'

            elif menu[0] == '1':
                _output = _output + '<li><a href="' + menu[1] + '"><i class="fa ' + menu[2] + ' fa-fw"></i> ' + menu[3] + '</a></li>'

            elif menu[0] == '2':
                _output = _output + '<li class="dropdown-sub"><a href="' + menu[1] + '">' + menu[3] + '</a></li>'

        _output = _output + '</ul></li>'

    results.append(_output)

    return results
