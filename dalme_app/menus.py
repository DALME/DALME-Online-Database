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
            ['1', 'Inventories', '/dashboard/list/inventories', 'fa-list', 'No', ''],
            ['1', 'Tools', '#', 'fa-wrench', 'Yes', ''],
                ['2', 'Wiki', 'http://dighist.fas.harvard.edu/projects/DALME/wiki', 'fa-book', 'No', ''],
                ['2', 'DAM', 'http://dighist.fas.harvard.edu/projects/DALME/dam', 'fa-image', 'No', 'Last'],
            ['1', 'Development', '#', 'fa-gear', 'Yes', ''],
                ['2', 'Testing', '#', 'fa-warning', 'Yes', 'Last'],
                    ['3', 'Inventory Ingestion', '/dashboard/upload/inventory', '', 'No', 'Last'],
            ]

    results = []
    _output = ''
    submenu = 0

    for item in menu:
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

            if item[5] == 'Last':
                submenu = 1

        results.append(_output)

    return results
