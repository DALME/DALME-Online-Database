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
    menu = [
            ['0', 'section-first', 'Modules', 'fa-th'],
            ['1', 'Inventories', '/dashboard/list/inventories', 'fa-list', 'No', ''],
            ['1', 'External Tools', '#', 'fa-wrench', 'Yes', ''],
                ['2', 'Wiki', 'http://dighist.fas.harvard.edu/projects/DALME/wiki', 'fa-book', 'No', ''],
                ['2', 'DAM', 'http://dighist.fas.harvard.edu/projects/DALME/dam', 'fa-image', 'No', 'Last'],
            ['0', 'section', 'Development', 'fa-gear'],
            ['1', 'Errors and Notifications', '/dashboard/list/errors', 'fa-medkit  ', 'No', ''],
            ['1', 'Testing', '#', 'fa-gears', 'No', ''],
            ['1', 'UI Reference', '#', 'fa-list-alt', 'Yes', 'Last'],
                ['2', 'Dashboard Content', '/dashboard/UIref/dash_demo', 'fa-dashboard', 'No', ''],
                ['2', 'Panels and Wells', '/dashboard/UIref/panels-wells', '', 'No', ''],
                ['2', 'Buttons', '/dashboard/UIref/buttons', '', 'No', ''],
                ['2', 'Notifications', '/dashboard/UIref/notifications', '', 'No', ''],
                ['2', 'Typography', '/dashboard/UIref/typography', '', 'No', ''],
                ['2', 'Icons', '/dashboard/UIref/icons', '', 'No', ''],
                ['2', 'Grid', '/dashboard/UIref/grid', '', 'No', ''],
                ['2', 'Tables', '/dashboard/UIref/tables', 'fa-table', 'No', ''],
                ['2', 'Flot Charts', '/dashboard/UIref/flot', 'fa-bar-chart-o', 'No', ''],
                ['2', 'Morris.js Charts', '/dashboard/UIref/morris', 'fa-bar-chart-o', 'No', ''],
                ['2', 'Forms', '/dashboard/UIref/forms', 'fa-edit', 'No', 'Last'],
            ]


    results = []
    _output = ''
    submenu = 0

    for item in menu:
        if item[0] == '0':
            _output = '<li class="sidebar-' + item[1] + '"><i class="fa ' + item[3] +' fa-fw"></i> ' + item[2] + '</li>'

        else:
            if item[4] == 'No':
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

                if item[0] == '1':
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
